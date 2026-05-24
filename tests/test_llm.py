"""Tests for the LLM client with mocked HTTP calls."""

from __future__ import annotations

import httpx
import pytest
import respx

from ai_commit.llm import call_llm

FAKE_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": "feat(foo): add hello function\n\nAdds a hello function."
            }
        }
    ]
}


@respx.mock
def test_call_llm_returns_content(monkeypatch):
    """call_llm returns the message content on success."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=FAKE_RESPONSE)
    )
    result = call_llm("Say hello", model="gpt-4o-mini")
    assert "feat(foo)" in result


@respx.mock
def test_call_llm_custom_base_url(monkeypatch):
    """call_llm respects OPENAI_BASE_URL env var."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://custom.llm.example/v1")
    respx.post("https://custom.llm.example/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=FAKE_RESPONSE)
    )
    result = call_llm("Hello", model="gpt-4o-mini")
    assert result  # any non-empty string is fine


@respx.mock
def test_call_llm_raises_on_error(monkeypatch):
    """call_llm raises RuntimeError on non-2xx response."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )
    with pytest.raises(RuntimeError, match="401"):
        call_llm("Hello")


@respx.mock
def test_call_llm_strips_whitespace(monkeypatch):
    """call_llm strips leading/trailing whitespace from the reply."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    response_with_whitespace = {
        "choices": [{"message": {"content": "  feat: trimmed  "}}]
    }
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=response_with_whitespace)
    )
    result = call_llm("prompt")
    assert result == "feat: trimmed"
