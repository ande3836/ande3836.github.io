#!/usr/bin/env bash
# Runs a hook script with whichever Python 3 is installed (python3 / python / py),
# so the same settings.json works on Windows (Git Bash), macOS, and Linux.
# If no Python is found the hook is skipped instead of blocking work.
script="$1"; shift
for c in python3 python py; do
  if "$c" -c 'import sys; sys.exit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
    exec "$c" "$(dirname "$0")/$script" "$@"
  fi
done
echo "Hook $script skipped: Python 3.8+ not found on PATH." >&2
exit 0
