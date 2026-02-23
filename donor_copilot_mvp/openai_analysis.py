"""OpenAI-powered donor profile analysis helpers."""

from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

SYSTEM_PROMPT = (
    "You are a nonprofit fundraising strategist. "
    "Review the donor profile and provide concise, actionable guidance."
)


def analyze_donor(profile: dict[str, Any]) -> str:
    """Return AI-generated donor strategy recommendations.

    Args:
        profile: Donor profile data loaded from JSON.

    Returns:
        A short analysis with suggested next steps.

    Raises:
        ValueError: If OPENAI_API_KEY is missing.
        RuntimeError: If the OpenAI API request fails.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please configure it in your environment.")

    client = OpenAI(api_key=api_key)

    user_prompt = (
        "Analyze this donor profile and provide:\n"
        "1) A likely motivation summary\n"
        "2) Recommended outreach approach\n"
        "3) Suggested ask range for next gift\n"
        "4) One personalized talking point\n\n"
        f"Donor profile:\n{json.dumps(profile, indent=2)}"
    )

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_output_tokens=500,
        )
        return response.output_text.strip()
    except Exception as exc:
        raise RuntimeError(f"OpenAI analysis request failed: {exc}") from exc
