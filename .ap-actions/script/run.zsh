#!/usr/bin/env zsh
set -euo pipefail

clear
# tmux clear-history -t '.2'

poetry run python -u tests/scripts/error.py | poetry run python src/spretty/main.py
