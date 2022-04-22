#!/usr/bin/env zsh
set -euo pipefail

run_bin=.ap-actions/script/run.zsh

nodemon                \
  --quiet              \
	--ext py,zsh         \
	--watch src          \
	--watch "${run_bin}" \
	--exec "${run_bin}"

#  vim: fdm=marker fmr=〈,〉
