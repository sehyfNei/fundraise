"""LLM donor analysis helpers."""

from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

SYSTEM_PROMPT = (
    "You are an expert nonprofit fundraising strategist. "
    "Given donor profile data, produce concise, practical recommendations."
)

PROVIDER_CONFIG: dict[str, dict[str, str]] = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "default_model": "gpt-5.2",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "default_model": "openai/gpt-oss-120b",
    },
}


def analyze_donor(
    donor: dict[str, Any],
    provider: str = "openai",
    model: str | None = None,
) -> str:
    """Generate an AI summary for a donor profile.

    Args:
        donor: Donor profile data as a dictionary.
        provider: LLM provider, supported values are ``openai`` and ``groq``.
        model: Optional model override.

    Returns:
        A generated summary and recommendations.

    Raises:
        ValueError: If provider/API key configuration is invalid.
        RuntimeError: If the API request fails.
    """
    selected_provider = provider.lower().strip()
    if selected_provider not in PROVIDER_CONFIG:
        allowed = ", ".join(sorted(PROVIDER_CONFIG))
        raise ValueError(f"Unsupported provider '{provider}'. Choose one of: {allowed}.")

    cfg = PROVIDER_CONFIG[selected_provider]
    api_key = os.getenv(cfg["api_key_env"])
    if not api_key:
        raise ValueError(f"{cfg['api_key_env']} is not set. Please configure it in your environment.")

    model_name = model or os.getenv("LLM_MODEL") or cfg["default_model"]
    client = OpenAI(api_key=api_key, base_url=cfg["base_url"])

    donor_payload = json.dumps(donor, indent=2)
    user_prompt = (
        "Analyze the donor data below and return markdown with these sections:\n"
        "## Motivation Summary\n"
        "## Outreach Strategy\n"
        "## Suggested Ask Range\n"
        "## Personalized Talking Point\n"
        "## Risks / Watchouts\n\n"
        f"Donor data (JSON):\n{donor_payload}"
    )

    try:
        response = client.responses.create(
            model=model_name,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_output_tokens=700,
        )
        return response.output_text.strip()
    except Exception as exc:
        raise RuntimeError(f"Donor analysis request failed: {exc}") from exc
