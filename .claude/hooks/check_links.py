#!/usr/bin/env python3
"""Check that every local link, image, iframe, and #anchor in the site's HTML
points at something that exists.

Usage
  python3 .claude/hooks/check_links.py            # check every *.html page
  python3 .claude/hooks/check_links.py page.html  # check specific pages
  python3 .claude/hooks/check_links.py --hook     # Claude Code PostToolUse hook:
                                                  # reads the tool call JSON from stdin

Exit codes: 0 = all good / nothing to check, 2 = broken references found
(exit 2 makes Claude Code show the message to Claude so it fixes them).
Standard library only, so it also runs in GitHub Actions.
"""
import json
import os
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URL_ATTRS = {"href", "src", "poster", "data-src"}
SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "javascript:", "data:", "//")


class RefParser(HTMLParser):
    """Collects URL attributes and element ids. HTML comments are ignored by
    HTMLParser, so commented-out sections are never reported."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []  # (line, attr, value)
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        for name, value in attrs:
            if name in ("id", "name") and value:
                self.ids.add(value)
            if name in URL_ATTRS and value:
                self.refs.append((line, name, value.strip()))
            if name == "srcset" and value:
                for part in value.split(","):
                    url = part.strip().split(" ")[0]
                    if url:
                        self.refs.append((line, name, url))

    handle_startendtag = handle_starttag


def parse(path):
    parser = RefParser()
    with open(path, encoding="utf-8", errors="replace") as fh:
        parser.feed(fh.read())
    return parser


def check_page(path, id_cache):
    problems = []
    page_dir = os.path.dirname(path)
    parser = parse(path)
    id_cache[os.path.abspath(path)] = parser.ids
    for line, attr, value in parser.refs:
        if value.lower().startswith(SKIP_SCHEMES) or value in ("#", ""):
            continue
        parts = urlsplit(value)
        rel = os.path.relpath(path, ROOT)
        if not parts.path:  # same-page anchor
            if parts.fragment and parts.fragment not in parser.ids and parts.fragment != "top":
                problems.append(f"{rel}:{line} {attr}=\"{value}\" -> no element with id \"{parts.fragment}\"")
            continue
        local = unquote(parts.path)
        target = os.path.join(ROOT, local.lstrip("/")) if local.startswith("/") else os.path.join(page_dir, local)
        target = os.path.normpath(target)
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            problems.append(f"{rel}:{line} {attr}=\"{value}\" -> file not found")
            continue
        if parts.fragment and target.endswith(".html"):
            key = os.path.abspath(target)
            if key not in id_cache:
                id_cache[key] = parse(target).ids
            if parts.fragment not in id_cache[key]:
                problems.append(f"{rel}:{line} {attr}=\"{value}\" -> no element with id \"{parts.fragment}\"")
    return problems


def pages_from_hook_stdin():
    """When run as a hook, Claude Code sends JSON describing the tool call."""
    raw = sys.stdin.read().strip()
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    path = (data.get("tool_input") or {}).get("file_path", "")
    if not path.endswith(".html"):
        return []  # edit to a non-HTML file: nothing to check
    # One page changed, but its links might be checked alongside the rest:
    # check every page so renamed/removed targets are caught too.
    return all_pages()


def all_pages():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in ("node_modules", "_site")]
        out += [os.path.join(dirpath, f) for f in filenames if f.endswith(".html")]
    return sorted(out)


def main():
    args = sys.argv[1:]
    if args == ["--hook"]:
        pages = pages_from_hook_stdin()
        if pages is None:
            pages = all_pages()
    elif args:
        pages = [os.path.abspath(a) for a in args]
    else:
        pages = all_pages()
    if not pages:
        return 0
    id_cache, problems = {}, []
    for page in pages:
        problems += check_page(page, id_cache)
    if problems:
        print("Broken references found:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 2
    if args != ["--hook"]:
        print(f"Links OK across {len(pages)} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
