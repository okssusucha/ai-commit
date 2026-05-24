# ai-commit

> AI を使ったコミットメッセージ生成・PR 要約・コードレビュー CLI ツール  
> AI-powered git commit messages, PR summaries & code review — zero config, OpenAI-compatible.

---

## 日本語

### これは何？

`ai-commit` は、ステージされた差分や PR の diff を LLM に渡して
- **コミットメッセージを自動生成**（Conventional Commits 準拠）
- **PR の変更内容を箇条書きで要約**
- **クイックコードレビュー**

を行うシンプルな CLI ツールです。OpenAI 互換 API をサポートするため、
OpenAI・Azure OpenAI・Ollama など任意のエンドポイントで動作します。

### インストール

```bash
# uv tool install（推奨）
uv tool install .

# または pipx
pipx install .
```

### 使い方

```bash
# ステージされた変更からコミットメッセージを生成
export OPENAI_API_KEY=sk-...
git add -p
ai-commit msg

# PR / diff を要約
ai-commit summary --base main

# コードレビュー
ai-commit review --base main

# API を呼ばずにプロンプトだけ確認（--dry-run）
ai-commit msg --dry-run
```

### 環境変数

| 変数名 | 説明 | 例 |
|---|---|---|
| `OPENAI_API_KEY` | API キー（必須） | `sk-...` |
| `OPENAI_BASE_URL` | ベース URL（省略時は OpenAI） | `http://localhost:11434/v1` |

---

## English

### What is this?

`ai-commit` is a lightweight CLI that pipes your git diffs to an LLM to:

- **Generate conventional commit messages** from staged changes
- **Summarise PRs** as bullet-point descriptions
- **Run a quick code review** on any diff

It talks to any OpenAI-compatible endpoint (OpenAI, Azure, Ollama, etc.).

### Install

```bash
# Recommended — uv tool install
uv tool install .

# Alternative
pipx install .
```

### Usage

```bash
export OPENAI_API_KEY=sk-...

# Generate a commit message from staged diff
git add -p
ai-commit msg

# Summarise changes vs. main
ai-commit summary --base main

# Code review vs. HEAD
ai-commit review

# Preview the prompt without hitting the API
ai-commit msg --dry-run
ai-commit review --dry-run
ai-commit summary --dry-run
```

### Demo

```
$ git add src/ai_commit/llm.py
$ ai-commit msg

Generating commit message...

Suggested commit message:
feat(llm): add OpenAI-compatible client with env-based config

Introduces a thin httpx wrapper that reads OPENAI_API_KEY and
OPENAI_BASE_URL from the environment, making the provider fully
swappable without code changes.

$ ai-commit summary --base main

Summarising diff...

Summary:
- Added call_llm function isolating all HTTP calls to one place
- Three CLI commands: msg, review, summary -- each with --dry-run
- 20 tests covering prompt assembly, LLM mocking, and CLI invocation
- CI on GitHub Actions (Python 3.11 & 3.12, ruff + pytest)

$ ai-commit review --base main

Reviewing diff...

Code review:
Good separation of concerns -- LLM call isolated in llm.py
--dry-run prevents accidental API usage in scripts
Consider adding retry logic for transient 5xx errors
Diff truncation may be needed for very large PRs
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `OPENAI_API_KEY` | Your API key | — |
| `OPENAI_BASE_URL` | API base URL | `https://api.openai.com/v1` |

### Architecture

```
src/ai_commit/
├── __init__.py     # version
├── cli.py          # typer app — msg / review / summary commands
├── git.py          # thin subprocess wrappers for git diff
├── llm.py          # single call_llm() function (easily mocked)
└── prompts.py      # pure prompt-assembly functions
tests/
├── test_cli.py     # CLI integration tests (CliRunner, monkeypatch)
├── test_llm.py     # HTTP mocking with respx
└── test_prompts.py # unit tests for prompt builders
```

### License

MIT — see [LICENSE](LICENSE).
