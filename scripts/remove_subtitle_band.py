#!/usr/bin/env python3
"""Remove hardcoded subtitle text with a small dynamic blur band.

The tool is intentionally conservative: it only changes a narrow lower-frame
band where subtitle-like bright text is detected. If detection fails, it falls
back to a fixed ratio band that can be overridden by --rect or --rect-ratio.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np


def parse_rect(value: str) -> tuple[float, float, float, float]:
    parts = value.split(":")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("expected X:Y:W:H")
    try:
        return tuple(float(p) for p in parts)  # type: ignore[return-value]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("rect values must be numbers") from exc


def clamp_rect(rect: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    x = max(0, min(width - 1, x))
    y = max(0, min(height - 1, y))
    w = max(1, min(width - x, w))
    h = max(1, min(height - y, h))
    return x, y, w, h


def ratio_rect(rect: tuple[float, float, float, float], width: int, height: int) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    return clamp_rect(
        (round(x * width), round(y * height), round(w * width), round(h * height)),
        width,
        height,
    )


def detect_subtitle_y(frame: np.ndarray, args: argparse.Namespace) -> int | None:
    """Return the detected subtitle-band center y, or None if confidence is low."""
    height, width = frame.shape[:2]
    search_y0 = round(height * args.search_y0)
    search_y1 = round(height * args.search_y1)
    search_x0 = round(width * args.search_x0)
    search_x1 = round(width * args.search_x1)

    roi = frame[search_y0:search_y1, search_x0:search_x1]
    if roi.size == 0:
        return None

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    base = cv2.inRange(
        hsv,
        np.array([0, 0, args.value_min], dtype=np.uint8),
        np.array([179, args.sat_max, 255], dtype=np.uint8),
    )

    # Keep glyph-like fragments and reject broad bright objects.
    count, labels, stats, _ = cv2.connectedComponentsWithStats(base, 8)
    clean = np.zeros_like(base)
    for idx in range(1, count):
        _x, _y, comp_w, comp_h, area = stats[idx]
        if (
            args.comp_min_w <= comp_w <= args.comp_max_w
            and args.comp_min_h <= comp_h <= args.comp_max_h
            and args.comp_min_area <= area <= args.comp_max_area
        ):
            clean[labels == idx] = 255

    if int((clean > 0).sum()) < args.min_mask_pixels:
        return None

    window = max(3, args.row_window)
    row_score = np.convolve(clean.sum(axis=1) / 255.0, np.ones(window) / window, mode="same")
    local_y = int(row_score.argmax())
    if float(row_score[local_y]) < args.min_row_score:
        return None

    return search_y0 + local_y


def smooth_center(prev: float | None, current: int | None, fallback: int, alpha: float) -> float:
    if current is None:
        return fallback if prev is None else prev
    if prev is None:
        return float(current)
    return prev * alpha + current * (1.0 - alpha)


def blur_rect(frame: np.ndarray, rect: tuple[int, int, int, int], args: argparse.Namespace) -> np.ndarray:
    x, y, w, h = rect
    output = frame.copy()
    patch = output[y : y + h, x : x + w]
    blurred = cv2.GaussianBlur(patch, (0, 0), sigmaX=args.sigma_x, sigmaY=args.sigma_y)

    feather = min(args.feather, h // 3, w // 3)
    alpha = np.ones((h, w), np.float32)
    for idx in range(feather):
        value = (idx + 1) / feather
        alpha[idx, :] *= value
        alpha[-idx - 1, :] *= value
        alpha[:, idx] *= value
        alpha[:, -idx - 1] *= value

    output[y : y + h, x : x + w] = (
        patch * (1.0 - alpha[..., None]) + blurred * alpha[..., None]
    ).astype(np.uint8)
    return output


def inpaint_rect(frame: np.ndarray, rect: tuple[int, int, int, int], args: argparse.Namespace) -> np.ndarray:
    x, y, w, h = rect
    mask = np.zeros(frame.shape[:2], np.uint8)
    mask[y : y + h, x : x + w] = 255
    return cv2.inpaint(frame, mask, args.inpaint_radius, cv2.INPAINT_TELEA)


def subtitle_text_mask(frame: np.ndarray, rect: tuple[int, int, int, int], args: argparse.Namespace) -> np.ndarray:
    x, y, w, h = rect
    roi = frame[y : y + h, x : x + w]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    base = cv2.inRange(
        hsv,
        np.array([0, 0, args.value_min], dtype=np.uint8),
        np.array([179, args.sat_max, 255], dtype=np.uint8),
    )

    count, labels, stats, _ = cv2.connectedComponentsWithStats(base, 8)
    clean = np.zeros_like(base)
    for idx in range(1, count):
        _x, _y, comp_w, comp_h, area = stats[idx]
        if (
            args.comp_min_w <= comp_w <= args.comp_max_w
            and args.comp_min_h <= comp_h <= args.comp_max_h
            and args.comp_min_area <= area <= args.comp_max_area
        ):
            clean[labels == idx] = 255

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (max(1, args.mask_dilate_x), max(1, args.mask_dilate_y)),
    )
    clean = cv2.dilate(clean, kernel, iterations=max(1, args.mask_dilate_iterations))

    mask = np.zeros(frame.shape[:2], np.uint8)
    mask[y : y + h, x : x + w] = clean
    return mask


def mask_inpaint_rect(frame: np.ndarray, rect: tuple[int, int, int, int], args: argparse.Namespace) -> np.ndarray:
    mask = subtitle_text_mask(frame, rect, args)
    if int((mask > 0).sum()) < args.min_mask_pixels:
        return frame

    repaired = cv2.inpaint(frame, mask, args.inpaint_radius, cv2.INPAINT_TELEA)
    if not args.mask_soften:
        return repaired

    softened = cv2.GaussianBlur(repaired, (0, 0), sigmaX=args.sigma_x, sigmaY=args.sigma_y)
    alpha = cv2.GaussianBlur(
        mask.astype(np.float32) / 255.0,
        (0, 0),
        sigmaX=args.mask_feather,
        sigmaY=max(1, args.mask_feather // 2),
    )
    return (repaired * (1.0 - alpha[..., None]) + softened * alpha[..., None]).astype(np.uint8)


def encode_video(input_path: Path, output_path: Path, args: argparse.Namespace) -> None:
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError(f"could not open input video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_name(f"{output_path.stem}.noaudio.{os.getpid()}.tmp.mp4")

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-s",
        f"{width}x{height}",
        "-r",
        f"{fps}",
        "-i",
        "-",
        "-c:v",
        "libx264",
        "-preset",
        args.preset,
        "-crf",
        str(args.crf),
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(tmp_path),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    if proc.stdin is None:
        raise RuntimeError("failed to open ffmpeg stdin")

    manual_rect = None
    if args.rect is not None:
        manual_rect = clamp_rect(tuple(round(v) for v in args.rect), width, height)

    fallback_rect = ratio_rect(args.rect_ratio, width, height)
    band_height = manual_rect[3] if manual_rect else fallback_rect[3]
    fallback_center = fallback_rect[1] + fallback_rect[3] // 2
    x = manual_rect[0] if manual_rect else fallback_rect[0]
    w = manual_rect[2] if manual_rect else fallback_rect[2]
    center: float | None = None
    frames = 0
    detected = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            if args.mode == "mask-inpaint" and args.auto and manual_rect is None:
                current = detect_subtitle_y(frame, args)
                if current is not None:
                    detected += 1
                    center = smooth_center(center, current, fallback_center, args.smooth)
                    y = round(center - band_height / 2)
                    rect = clamp_rect((x, y, w, band_height), width, height)
                    frame = mask_inpaint_rect(frame, rect, args)
            elif manual_rect is not None or not args.auto:
                rect = manual_rect or fallback_rect
                if args.mode == "inpaint":
                    frame = inpaint_rect(frame, rect, args)
                elif args.mode == "mask-inpaint":
                    frame = mask_inpaint_rect(frame, rect, args)
                else:
                    frame = blur_rect(frame, rect, args)
            else:
                current = detect_subtitle_y(frame, args)
                if current is not None:
                    detected += 1
                center = smooth_center(center, current, fallback_center, args.smooth)
                y = round(center - band_height / 2)
                rect = clamp_rect((x, y, w, band_height), width, height)
                if args.mode == "inpaint":
                    frame = inpaint_rect(frame, rect, args)
                else:
                    frame = blur_rect(frame, rect, args)

            proc.stdin.write(frame.tobytes())
            frames += 1
            if args.verbose and total > 0 and frames % 100 == 0:
                print(f"processed {frames}/{total} frames", file=sys.stderr)
    finally:
        cap.release()
        proc.stdin.close()

    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"ffmpeg video encode failed with exit code {ret}")

    mux_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(tmp_path),
        "-i",
        str(input_path),
        "-map",
        "0:v:0",
        "-map",
        "1:a?",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    subprocess.run(mux_cmd, check=True)
    tmp_path.unlink(missing_ok=True)

    print(output_path)
    print(
        f"frames={frames} size={width}x{height} fps={fps:.3f} "
        f"fallback_rect={fallback_rect[0]}:{fallback_rect[1]}:{fallback_rect[2]}:{fallback_rect[3]} "
        f"auto_detected={detected if args.auto and manual_rect is None else 'off'}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remove hardcoded subtitles by blurring or inpainting a small subtitle band.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="Input video path")
    parser.add_argument("output", type=Path, help="Output video path")
    parser.add_argument("--mode", choices=("blur", "inpaint", "mask-inpaint"), default="blur")
    parser.add_argument("--rect", type=parse_rect, help="Manual absolute X:Y:W:H subtitle band")
    parser.add_argument(
        "--rect-ratio",
        type=parse_rect,
        default=(0.055, 0.791, 0.890, 0.095),
        help="Fallback ratio X:Y:W:H subtitle band",
    )
    parser.add_argument("--auto", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--search-y0", type=float, default=0.65, help="Auto-detect search top ratio")
    parser.add_argument("--search-y1", type=float, default=0.96, help="Auto-detect search bottom ratio")
    parser.add_argument("--search-x0", type=float, default=0.04, help="Auto-detect search left ratio")
    parser.add_argument("--search-x1", type=float, default=0.96, help="Auto-detect search right ratio")
    parser.add_argument("--value-min", type=int, default=145, help="Minimum HSV value for light text")
    parser.add_argument("--sat-max", type=int, default=120, help="Maximum HSV saturation for light text")
    parser.add_argument("--comp-min-w", type=int, default=2)
    parser.add_argument("--comp-max-w", type=int, default=90)
    parser.add_argument("--comp-min-h", type=int, default=3)
    parser.add_argument("--comp-max-h", type=int, default=36)
    parser.add_argument("--comp-min-area", type=int, default=8)
    parser.add_argument("--comp-max-area", type=int, default=1000)
    parser.add_argument("--min-mask-pixels", type=int, default=80)
    parser.add_argument("--row-window", type=int, default=13)
    parser.add_argument("--min-row-score", type=float, default=40)
    parser.add_argument("--smooth", type=float, default=0.88, help="Temporal smoothing factor for band y")
    parser.add_argument("--sigma-x", type=float, default=18)
    parser.add_argument("--sigma-y", type=float, default=10)
    parser.add_argument("--feather", type=int, default=18)
    parser.add_argument("--inpaint-radius", type=int, default=5)
    parser.add_argument("--mask-dilate-x", type=int, default=13)
    parser.add_argument("--mask-dilate-y", type=int, default=7)
    parser.add_argument("--mask-dilate-iterations", type=int, default=2)
    parser.add_argument("--mask-feather", type=int, default=3)
    parser.add_argument(
        "--mask-soften",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Blur the repaired mask area after inpainting; disable to avoid dark soft patches.",
    )
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--preset", default="medium")
    parser.add_argument("--verbose", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.input.exists():
        parser.error(f"input does not exist: {args.input}")
    if not shutil_available("ffmpeg"):
        parser.error("ffmpeg is required but was not found in PATH")
    encode_video(args.input, args.output, args)
    return 0


def shutil_available(binary: str) -> bool:
    from shutil import which

    return which(binary) is not None


if __name__ == "__main__":
    raise SystemExit(main())
