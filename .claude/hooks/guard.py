#!/usr/bin/env python3
"""PreToolUse guard: blocks the few actions that can break the live site.

- Editing the GitHub Pages deploy workflow (.github/workflows/*)
- Force-pushing (rewrites history on the branch that deploys)

Exit 2 blocks the tool call and shows the reason to Claude; exit 0 allows it.
"""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError):
    sys.exit(0)

tool = data.get("tool_name", "")
inp = data.get("tool_input") or {}

if tool in ("Edit", "Write", "MultiEdit"):
    path = inp.get("file_path", "").replace("\\", "/")
    if "/.github/workflows/" in path or path.startswith(".github/workflows/"):
        print("Blocked: .github/workflows/ controls the live GitHub Pages deploy. "
              "Explain the change to Andrew and get an explicit OK before editing it.", file=sys.stderr)
        sys.exit(2)

if tool == "Bash":
    cmd = inp.get("command", "")
    if re.search(r"\bgit\s+push\b", cmd) and re.search(r"(\s--force(-with-lease)?\b|\s-f\b|\s\+\S+)", cmd):
        print("Blocked: force-pushing rewrites the history that GitHub Pages deploys from. "
              "Use a normal push, or ask Andrew first.", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
