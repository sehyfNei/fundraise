"""Streamlit MVP app for donor profile analysis."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from openai_analysis import analyze_donor_profile

PROFILE_PATH = Path(__file__).with_name("sample_donor_profile.json")


@st.cache_data
def load_profile(path: Path) -> dict:
    """Load and parse a donor profile JSON file."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    """Render the donor copilot app."""
    st.set_page_config(page_title="Donor Copilot MVP", page_icon="🎯", layout="wide")
    st.title("🎯 Donor Copilot MVP")
    st.caption("View a donor profile and generate AI-driven fundraising recommendations.")

    profile = load_profile(PROFILE_PATH)

    col_profile, col_analysis = st.columns([1, 1], gap="large")

    with col_profile:
        st.subheader("Sample Donor Profile")
        st.json(profile)

    with col_analysis:
        st.subheader("AI Analysis")
        if st.button("Generate analysis", type="primary"):
            with st.spinner("Analyzing donor profile..."):
                try:
                    analysis = analyze_donor_profile(profile)
                    st.success("Analysis complete")
                    st.markdown(analysis)
                except Exception as exc:
                    st.error(str(exc))

    with st.expander("Setup"):
        st.code(
            "\n".join(
                [
                    "pip install -r requirements.txt",
                    "export OPENAI_API_KEY=your_key_here",
                    "streamlit run app.py",
                ]
            ),
            language="bash",
        )


if __name__ == "__main__":
    main()
