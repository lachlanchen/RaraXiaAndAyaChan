# Xiaoyunque Paid Generation Quality Gate

## Purpose

Prevent an unverified model, storyboard, or character mapping from consuming
credits or reaching publication. This is a general workflow rule, not a prompt
for one episode.

## Incident Evidence

The 2026-08-23 earthquake episode exposed four independent failures:

1. The long Agent flow expanded a requested short story into 13 shots and about
   68 seconds.
2. The visible storyboard used a warm 2D cartoon style although the uploaded
   references required realistic toy figurines.
3. The material-analysis step timed out, but the workflow continued from text
   instead of stopping on missing reference evidence.
4. The resulting 70.543-second video replaced the main cast with generic
   mascots/human children. The render cost 67 credits.

The rejected artifact and contact sheet remain local evidence. No public
platform publish job was queued for it.

## Required Preflight

Before clicking any paid generation button, capture one screenshot showing:

- current workflow or mode;
- actual selected model and tier;
- duration and aspect ratio;
- every required attachment preview in the intended order;
- filled prompt;
- displayed cost and current balance;
- automatic generation countdown disabled.

Prompt text is not configuration evidence. Agent chat claims are not editor
state evidence.

For storyboard workflows, inspect the real storyboard before rendering. Stop
when style, duration, shot count, or character mapping differs from the request.

## Required Acceptance

After download and before another paid clip or publication:

1. Probe duration, dimensions, and streams with `ffprobe`.
2. Decode the full file with `ffmpeg`.
3. Generate and inspect a contact sheet.
4. Confirm each named main character matches its uploaded individual reference.
5. Confirm no duplicate/replacement lead and no style switch.
6. Confirm the requested story setting and key beats are visible.

Rejected outputs stay as local evidence and never enter AutoPublish unless the
user explicitly requests that exact file.

## Multi-Clip Recovery

When a direct short-video workflow is safer than a drifting long Agent flow:

- show the total visible credit cost before starting;
- generate only the first clip;
- validate its character identity and style;
- stop immediately if it fails;
- spend on later clips only after the first passes;
- concatenate only accepted clips.

This makes the first clip a quality gate rather than spending the whole budget
before discovering the same failure in every segment.
