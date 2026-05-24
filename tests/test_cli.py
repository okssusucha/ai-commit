"""CLI tests using typer's CliRunner — all LLM calls mocked."""

from __future__ import annotations

from typer.testing import CliRunner

from ai_commit.cli import app

runner = CliRunner()

SAMPLE_DIFF = """\
diff --git a/foo.py b/foo.py
index 0000000..1111111 100644
--- a/foo.py
+++ b/foo.py
@@ -1,3 +1,5 @@
 def hello():
-    pass
+    print("hello")
"""


# ---------------------------------------------------------------------------
# msg command
# ---------------------------------------------------------------------------


def test_msg_dry_run(monkeypatch):
    """--dry-run prints the prompt without calling the LLM."""
    monkeypatch.setattr("ai_commit.git.get_staged_diff", lambda: SAMPLE_DIFF)
    result = runner.invoke(app, ["msg", "--dry-run"])
    assert result.exit_code == 0
    assert "dry-run" in result.output.lower() or "PROMPT" in result.output


def test_msg_calls_llm(monkeypatch):
    """msg command calls the LLM and prints the response."""
    monkeypatch.setattr("ai_commit.git.get_staged_diff", lambda: SAMPLE_DIFF)
    monkeypatch.setattr(
        "ai_commit.llm.call_llm",
        lambda prompt, model="gpt-4o-mini": "feat: add hello",
    )
    result = runner.invoke(app, ["msg"])
    assert result.exit_code == 0
    assert "feat: add hello" in result.output


def test_msg_empty_diff_exits_nonzero(monkeypatch):
    """msg command exits 1 when there is no staged diff."""
    monkeypatch.setattr("ai_commit.git.get_staged_diff", lambda: "")
    result = runner.invoke(app, ["msg"])
    assert result.exit_code != 0


def test_msg_llm_error_exits_nonzero(monkeypatch):
    """msg command exits 1 when the LLM raises RuntimeError."""
    monkeypatch.setattr("ai_commit.git.get_staged_diff", lambda: SAMPLE_DIFF)
    monkeypatch.setattr(
        "ai_commit.llm.call_llm",
        lambda prompt, model="gpt-4o-mini": (_ for _ in ()).throw(
            RuntimeError("API error")
        ),
    )
    result = runner.invoke(app, ["msg"])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# review command
# ---------------------------------------------------------------------------


def test_review_dry_run(monkeypatch):
    """review --dry-run prints the prompt without calling the LLM."""
    monkeypatch.setattr("ai_commit.git.get_diff", lambda base="HEAD": SAMPLE_DIFF)
    result = runner.invoke(app, ["review", "--dry-run"])
    assert result.exit_code == 0
    assert "PROMPT" in result.output or "dry" in result.output.lower()


def test_review_calls_llm(monkeypatch):
    """review command calls the LLM and prints the response."""
    monkeypatch.setattr("ai_commit.git.get_diff", lambda base="HEAD": SAMPLE_DIFF)
    monkeypatch.setattr(
        "ai_commit.llm.call_llm",
        lambda prompt, model="gpt-4o-mini": "Looks good!",
    )
    result = runner.invoke(app, ["review"])
    assert result.exit_code == 0
    assert "Looks good!" in result.output


def test_review_empty_diff_exits_nonzero(monkeypatch):
    """review exits 1 when there is no diff."""
    monkeypatch.setattr("ai_commit.git.get_diff", lambda base="HEAD": "")
    result = runner.invoke(app, ["review"])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# summary command
# ---------------------------------------------------------------------------


def test_summary_dry_run(monkeypatch):
    """summary --dry-run prints the prompt without calling the LLM."""
    monkeypatch.setattr("ai_commit.git.get_diff", lambda base="HEAD": SAMPLE_DIFF)
    result = runner.invoke(app, ["summary", "--dry-run"])
    assert result.exit_code == 0
    assert "PROMPT" in result.output or "dry" in result.output.lower()


def test_summary_calls_llm(monkeypatch):
    """summary command calls the LLM and prints the response."""
    monkeypatch.setattr("ai_commit.git.get_diff", lambda base="HEAD": SAMPLE_DIFF)
    monkeypatch.setattr(
        "ai_commit.llm.call_llm",
        lambda prompt, model="gpt-4o-mini": "- Added hello function",
    )
    result = runner.invoke(app, ["summary"])
    assert result.exit_code == 0
    assert "Added hello function" in result.output


def test_summary_empty_diff_exits_nonzero(monkeypatch):
    """summary exits 1 when there is no diff."""
    monkeypatch.setattr("ai_commit.git.get_diff", lambda base="HEAD": "")
    result = runner.invoke(app, ["summary"])
    assert result.exit_code != 0
