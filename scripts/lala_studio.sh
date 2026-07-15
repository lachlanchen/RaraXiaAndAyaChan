#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
STUDIO_DIR="$(cd -- "$SCRIPT_DIR/../studio" && pwd)"

if [[ ! -d "$STUDIO_DIR/node_modules" ]]; then
  npm --prefix "$STUDIO_DIR" install
fi

case "${1:-dev}" in
  dev)
    exec npm --prefix "$STUDIO_DIR" run dev
    ;;
  serve)
    npm --prefix "$STUDIO_DIR" run build
    exec npm --prefix "$STUDIO_DIR" start
    ;;
  build)
    exec npm --prefix "$STUDIO_DIR" run build
    ;;
  test)
    exec npm --prefix "$STUDIO_DIR" test
    ;;
  *)
    exec npm --prefix "$STUDIO_DIR" run cli -- "$@"
    ;;
esac
