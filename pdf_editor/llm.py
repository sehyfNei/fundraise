from __future__ import annotations

import json
import os
from urllib import error, request


GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"


def rewrite_text_with_llm(original_text: str, style: str | None = None) -> str:
    """
    Rewrite text using Groq if GROQ_API_KEY is configured.

    Fallback behavior (no key/network issue): return deterministic placeholder rewrite,
    so the app remains usable in local/offline environments.
    """
    chosen_style = style or "clear"
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return f"[{chosen_style} rewrite] {original_text}"

    prompt = (
        f"Rewrite the following text in a {chosen_style} tone. "
        "Keep facts and meaning unchanged. Return only rewritten text.\n\n"
        f"Text:\n{original_text}"
    )

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise document rewriting assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    req = request.Request(
        GROQ_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=20) as resp:  # noqa: S310
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"].strip()
    except (error.URLError, error.HTTPError, KeyError, IndexError, json.JSONDecodeError):
        return f"[{chosen_style} rewrite] {original_text}"
