"""Streamlit MVP app for donor profile analysis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from openai_analysis import analyze_donor

DONOR_PATH = Path(__file__).with_name("donor.json")


@st.cache_data
def load_donor(path: Path) -> dict[str, Any]:
    """Load and parse a donor JSON file."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def render_sidebar(donor: dict[str, Any]) -> None:
    """Render donor fields in the Streamlit sidebar."""
    st.sidebar.header("Donor Details")
    st.sidebar.write(f"**Donor ID:** {donor.get('donor_id', 'N/A')}")
    st.sidebar.write(f"**Name:** {donor.get('name', 'N/A')}")
    st.sidebar.write(f"**Location:** {donor.get('location', 'N/A')}")
    st.sidebar.write(f"**Preferred Contact:** {donor.get('preferred_contact', 'N/A')}")
    st.sidebar.write(f"**Lifetime Giving (USD):** {donor.get('lifetime_giving_usd', 'N/A')}")

    last_gift = donor.get("last_gift", {})
    st.sidebar.subheader("Last Gift")
    st.sidebar.write(f"Amount: {last_gift.get('amount_usd', 'N/A')}")
    st.sidebar.write(f"Date: {last_gift.get('date', 'N/A')}")
    st.sidebar.write(f"Campaign: {last_gift.get('campaign', 'N/A')}")


def main() -> None:
    """Render the donor copilot app."""
    st.set_page_config(page_title="Donor Copilot MVP", page_icon="🎯")
    st.title("🎯 Donor Copilot MVP")

    donor = load_donor(DONOR_PATH)
    render_sidebar(donor)

    st.subheader("Donor JSON")
    st.json(donor)

    if st.button("Analyze Donor", type="primary"):
        with st.spinner("Analyzing donor..."):
            try:
                analysis = analyze_donor(donor)
                st.session_state["analysis"] = analysis
            except Exception as exc:
                st.session_state["analysis"] = f"Error: {exc}"

    if "analysis" in st.session_state:
        st.subheader("AI Output")
        st.write(st.session_state["analysis"])


if __name__ == "__main__":
    main()
