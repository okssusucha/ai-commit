"""Tests for prompt assembly functions."""

from __future__ import annotations

from ai_commit.prompts import (
    build_commit_prompt,
    build_review_prompt,
    build_summary_prompt,
)

SAMPLE_DIFF = """\
diff --git a/foo.py b/foo.py
index 0000000..1111111 100644
--- a/foo.py
+++ b/foo.py
@@ -1,3 +1,5 @@
 def hello():
-    pass
+    print("hello")
+
+hello()
"""


def test_commit_prompt_contains_diff():
    prompt = build_commit_prompt(SAMPLE_DIFF)
    assert SAMPLE_DIFF in prompt
    assert "commit message" in prompt.lower()


def test_review_prompt_contains_diff():
    prompt = build_review_prompt(SAMPLE_DIFF)
    assert SAMPLE_DIFF in prompt
    assert "review" in prompt.lower()


def test_summary_prompt_contains_diff():
    prompt = build_summary_prompt(SAMPLE_DIFF)
    assert SAMPLE_DIFF in prompt
    assert "summar" in prompt.lower()


def test_commit_prompt_structure():
    prompt = build_commit_prompt(SAMPLE_DIFF)
    assert "BEGIN DIFF" in prompt
    assert "END DIFF" in prompt


def test_review_prompt_structure():
    prompt = build_review_prompt(SAMPLE_DIFF)
    assert "BEGIN DIFF" in prompt
    assert "END DIFF" in prompt


def test_summary_prompt_structure():
    prompt = build_summary_prompt(SAMPLE_DIFF)
    assert "BEGIN DIFF" in prompt
    assert "END DIFF" in prompt
