#!/usr/bin/env zsh
set -euo pipefail

poetry build && pip install --force-reinstall dist/*.whl
