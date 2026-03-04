from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from pdf_editor.editor import apply_command
from pdf_editor.generator import generate_pdf
from pdf_editor.interpreter import InstructionParseError, interpret_instruction
from pdf_editor.parser import parse_pdf


st.set_page_config(page_title="LLM PDF Editor MVP", layout="wide")
st.title("LLM Controlled PDF Editor (MVP)")
st.caption("Edit PDFs with plain-English instructions (replace/rewrite).")

with st.sidebar:
    st.subheader("How to use")
    st.markdown(
        """
1. Upload a PDF.
2. Check extracted paragraph IDs.
3. Enter an instruction.
4. Click **Apply instruction**.
5. Download the edited PDF.

**Supported examples**
- `replace all "Company A" with "Company B"`
- `rewrite paragraph 2 in professional tone`
        """
    )

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
instruction = st.text_input("Instruction", placeholder='e.g. replace all "A" with "B"')

if uploaded is not None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = Path(tmp_dir) / uploaded.name
        input_path.write_bytes(uploaded.read())

        document = parse_pdf(str(input_path), uploaded.name)

        paragraph_blocks = [b for b in document.blocks if b.id.startswith("paragraph_")]
        with st.expander("Extracted paragraph IDs (for rewrite targeting)", expanded=True):
            if paragraph_blocks:
                st.table(
                    [
                        {"id": b.id, "page": b.page, "preview": b.text[:120]}
                        for b in paragraph_blocks
                    ]
                )
            else:
                st.info("No paragraph blocks detected in this PDF.")

        with st.expander("Full parsed blocks (debug view)"):
            st.json(document.to_dict())

        if st.button("Apply instruction"):
            if not instruction.strip():
                st.warning("Please provide an instruction")
            else:
                try:
                    command = interpret_instruction(instruction)
                    st.info(f"Interpreted command: {command.to_dict()}")

                    edited_document = apply_command(document, command)

                    output_path = Path(tmp_dir) / f"edited_{uploaded.name}"
                    generate_pdf(edited_document, str(output_path))

                    st.success("Edit applied successfully.")
                    st.download_button(
                        "Download edited PDF",
                        data=output_path.read_bytes(),
                        file_name=output_path.name,
                        mime="application/pdf",
                    )
                except InstructionParseError as err:
                    st.error(str(err))
                except Exception as err:  # noqa: BLE001
                    st.error(f"Failed to apply edit: {err}")
