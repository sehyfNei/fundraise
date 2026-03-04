from __future__ import annotations


def rewrite_text_with_llm(original_text: str, style: str | None = None) -> str:
    """
    Placeholder rewriting function.

    Replace this with real LLM integration (OpenAI/Gemini/Ollama) in production.
    """
    chosen_style = style or "clear"
    return f"[{chosen_style} rewrite] {original_text}"
