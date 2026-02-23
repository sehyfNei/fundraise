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


def analyze_donor(donor: dict[str, Any]) -> str:
    """Generate an AI summary for a donor profile.

    Args:
        donor: Donor profile data as a dictionary.

    Returns:
        A generated summary and recommendations.

    Raises:
        ValueError: If OPENAI_API_KEY is missing.
        RuntimeError: If the API request fails.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please configure it in your environment.")

    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    client = OpenAI(api_key=api_key)

    donor_payload = json.dumps(donor, indent=2)
    user_prompt = (
        "Analyze the donor data below and return:\n"
        "1) Donor motivation summary\n"
        "2) Recommended outreach strategy\n"
        "3) Suggested ask range for the next gift\n"
        "4) One personalized talking point\n\n"
        f"Donor data (JSON):\n{donor_payload}"
    )

    try:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_output_tokens=500,
        )
        return response.output_text.strip()
    except Exception as exc:
        raise RuntimeError(f"Donor analysis request failed: {exc}") from exc
