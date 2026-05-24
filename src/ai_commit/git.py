"""Git helpers — thin wrappers around subprocess calls."""

from __future__ import annotations

import subprocess


def get_staged_diff() -> str:
    """Return the output of `git diff --staged`."""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def get_diff(base: str = "HEAD") -> str:
    """Return diff between *base* and the working tree."""
    result = subprocess.run(
        ["git", "diff", base],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout
