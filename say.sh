#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/src/main.py" "$@"
