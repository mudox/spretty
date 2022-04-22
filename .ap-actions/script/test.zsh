#!/usr/bin/env zsh
set -euo pipefail

clear
# tmux clear-history -t '.2'

pattern='check_level'
case 2 in
1) # Run given test
  poetry run pytest \
    --pdb           \
    --durations=0   \
    -vv             \
    -k "${pattern}"

  ;;
2) # Run all tests
  poetry run pytest \
		--pdb

  ;;
3) # Run tests marked by ``@pytest.mark.x`
  poetry run pytest \
    --pdb           \
    --durations=0   \
    -vv             \
    -m x

  ;;
esac
