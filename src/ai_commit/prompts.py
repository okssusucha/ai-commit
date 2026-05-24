"""Prompt assembly functions — pure, easily testable."""

from __future__ import annotations

_COMMIT_MSG_SYSTEM = """\
You are an expert software engineer. Given a git diff, write a concise \
conventional commit message (type(scope): subject, then a blank line, then an \
optional body). Output ONLY the commit message, no extra commentary."""

_REVIEW_SYSTEM = """\
You are a senior code reviewer. Review the following diff for bugs, security \
issues, style problems, and improvement opportunities. Be concise and \
constructive."""

_SUMMARY_SYSTEM = """\
You are a technical writer. Summarise the following diff or PR in 3-5 bullet \
points suitable for a pull-request description. Focus on *what* changed and \
*why*."""


def build_commit_prompt(diff: str) -> str:
    """Return the full prompt for generating a commit message from *diff*."""
    return (
        f"{_COMMIT_MSG_SYSTEM}\n\n"
        f"--- BEGIN DIFF ---\n{diff}\n--- END DIFF ---\n\n"
        "Commit message:"
    )


def build_review_prompt(diff: str) -> str:
    """Return the full prompt for reviewing *diff*."""
    return (
        f"{_REVIEW_SYSTEM}\n\n"
        f"--- BEGIN DIFF ---\n{diff}\n--- END DIFF ---\n\n"
        "Review:"
    )


def build_summary_prompt(diff: str) -> str:
    """Return the full prompt for summarising *diff*."""
    return (
        f"{_SUMMARY_SYSTEM}\n\n"
        f"--- BEGIN DIFF ---\n{diff}\n--- END DIFF ---\n\n"
        "Summary:"
    )
