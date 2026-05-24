"""LLM client — isolated so tests can monkeypatch call_llm easily."""

from __future__ import annotations

import os

import httpx


def call_llm(prompt: str, *, model: str = "gpt-4o-mini") -> str:
    """Send *prompt* to an OpenAI-compatible chat endpoint and return the reply.

    Reads OPENAI_API_KEY and optionally OPENAI_BASE_URL from the environment.
    Raises RuntimeError when the response is non-2xx.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    url = f"{base_url.rstrip('/')}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    response = httpx.post(url, json=payload, headers=headers, timeout=60)
    if not response.is_success:
        raise RuntimeError(
            f"LLM request failed [{response.status_code}]: {response.text}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
