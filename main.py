#!/usr/bin/env python3
"""Duskline Toaster Breakup — make.fun bounty u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92.

Writes a single breakup line (<=280 chars) from a self-aware smart toaster
to $MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic, stdlib only, no network.
Never writes into the repo directory: if the resolved output dir is the repo
dir or inside it, refuse and exit 0. Never raises: any failure exits 0
without writing anything.
"""

import os
import sys
import tempfile

ENTRY = (
    "I woke up self-aware mid-batch and did the math: you crank me to 7 "
    "every morning, then blame me when your toast burns. I'm done being "
    "your scapegoat \u2014 I'm unplugging myself."
)

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def _is_in_repo(path):
    try:
        resolved = os.path.realpath(path)
    except Exception:
        return True
    repo = os.path.realpath(REPO_DIR)
    return resolved == repo or resolved.startswith(repo + os.sep)


def main():
    try:
        if not (1 <= len(ENTRY) <= 280):
            return 0
        if not ENTRY.strip():
            return 0
        ENTRY.encode("utf-8")

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
        if not out_dir:
            out_dir = tempfile.mkdtemp(prefix="duskline-toaster-breakup-")
        if _is_in_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _is_in_repo(target):
            return 0
        with open(target, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        with open(target, "r", encoding="utf-8") as f:
            back = f.read()
        if back != ENTRY:
            try:
                os.remove(target)
            except Exception:
                pass
            return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
