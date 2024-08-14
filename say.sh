#!/usr/bin/env bash

export PYTHONWARNINGS="ignore"

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/src/main.py" "$@" || /usr/bin/say -v Samantha "$@"
