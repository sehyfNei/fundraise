"""Streamlit MVP app for donor profile analysis."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from analysis import PROVIDER_CONFIG, analyze_donor

DONOR_PATH = Path(__file__).with_name("donor.json")

load_dotenv()


@st.cache_data
def load_donor(path: Path) -> dict[str, Any]:
    """Load and parse a donor JSON file."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def render_sidebar(donor: dict[str, Any]) -> tuple[str, str]:
    """Render donor fields and app controls in the Streamlit sidebar."""
    st.sidebar.header("Donor Details")
    st.sidebar.write(f"**Donor ID:** {donor.get('donor_id', 'N/A')}")
    st.sidebar.write(f"**Name:** {donor.get('name', 'N/A')}")
    st.sidebar.write(f"**Location:** {donor.get('location', 'N/A')}")
    st.sidebar.write(f"**Preferred Contact:** {donor.get('preferred_contact', 'N/A')}")
    st.sidebar.write(f"**Lifetime Giving (USD):** {donor.get('lifetime_giving_usd', 'N/A')}")

    last_gift = donor.get("last_gift", {})
    st.sidebar.subheader("Last Gift")
    st.sidebar.write(f"Amount: ${last_gift.get('amount_usd', 'N/A')}")
    st.sidebar.write(f"Date: {last_gift.get('date', 'N/A')}")
    st.sidebar.write(f"Campaign: {last_gift.get('campaign', 'N/A')}")

    st.sidebar.subheader("Interests")
    for interest in donor.get("interests", []):
        st.sidebar.markdown(f"- {interest}")

    with st.sidebar.expander("Engagement Notes"):
        for note in donor.get("engagement_notes", []):
            st.markdown(f"- {note}")

    st.sidebar.divider()
    st.sidebar.subheader("AI Settings")
    provider = st.sidebar.selectbox("Provider", options=list(PROVIDER_CONFIG), index=0)
    default_model = PROVIDER_CONFIG[provider]["default_model"]
    model = st.sidebar.text_input("Model", value=os.getenv("LLM_MODEL", default_model))

    return provider, model


def validate_api_key(provider: str) -> None:
    """Show a warning if required API key for selected provider is missing."""
    key_env = PROVIDER_CONFIG[provider]["api_key_env"]
    if not os.getenv(key_env):
        st.warning(f"Set `{key_env}` to run analysis.")


def main() -> None:
    """Render the donor copilot app."""
    st.set_page_config(page_title="Donor Copilot MVP", page_icon="🎯")
    st.title("🎯 Donor Copilot MVP")
    st.caption("Analyze a donor profile with OpenAI or Groq-compatible models.")

    donor = load_donor(DONOR_PATH)
    provider, model = render_sidebar(donor)
    validate_api_key(provider)

    st.subheader("Donor JSON")
    st.json(donor)

    if "analysis_history" not in st.session_state:
        st.session_state["analysis_history"] = []

    if st.button("Analyze Donor", type="primary"):
        with st.spinner("Analyzing donor..."):
            try:
                analysis = analyze_donor(donor=donor, provider=provider, model=model)
                st.session_state["analysis"] = analysis
                st.session_state["analysis_history"].append(
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "provider": provider,
                        "model": model,
                        "analysis": analysis,
                    }
                )
            except Exception as exc:
                st.session_state["analysis"] = f"Error: {exc}"

    if "analysis" in st.session_state:
        st.subheader("AI Output")
        st.markdown(st.session_state["analysis"])
        st.download_button(
            label="Download latest analysis",
            data=st.session_state["analysis"],
            file_name="donor_analysis.md",
            mime="text/markdown",
        )

    if st.session_state["analysis_history"]:
        with st.expander("Analysis History"):
            for idx, item in enumerate(reversed(st.session_state["analysis_history"]), start=1):
                st.markdown(
                    f"**Run {idx}** — `{item['timestamp']}` via `{item['provider']}` / `{item['model']}`"
                )


if __name__ == "__main__":
    main()
