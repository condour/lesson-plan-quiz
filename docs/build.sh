#!/usr/bin/env bash
# Rebuild docs/index.html from ~/article/knowing-is-half-the-battle.md
# Source of truth is the markdown. index.html is generated - do not edit it.
set -e
python3 "$(dirname "$0")/build.py"
echo "built: $(dirname "$0")/index.html"
