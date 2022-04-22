#!/usr/bin/env zsh
set -euo pipefail

test_bin=.ap-actions/script/test.zsh

nodemon                 \
  --quiet               \
	--ext py,zsh          \
	--watch src           \
	--watch tests         \
	--watch "${test_bin}" \
	--exec "${test_bin}"

#  vim: fdm=marker fmr=〈,〉
