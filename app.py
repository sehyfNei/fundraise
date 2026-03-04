from __future__ import annotations

import json
import tempfile
from pathlib import Path

import streamlit as st

from pdf_editor.editor import apply_command
from pdf_editor.generator import generate_pdf
from pdf_editor.interpreter import InstructionParseError, interpret_instruction
from pdf_editor.parser import parse_pdf


st.set_page_config(page_title="LLM PDF Editor MVP", layout="wide")
st.title("LLM Controlled PDF Editor (MVP)")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
instruction = st.text_input("Instruction", placeholder='e.g. replace all "A" with "B"')

if uploaded is not None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = Path(tmp_dir) / uploaded.name
        input_path.write_bytes(uploaded.read())

        document = parse_pdf(str(input_path), uploaded.name)

        with st.expander("Parsed blocks"):
            st.json(document.to_dict())

        if st.button("Apply instruction"):
            if not instruction.strip():
                st.warning("Please provide an instruction")
            else:
                try:
                    command = interpret_instruction(instruction)
                    edited_document = apply_command(document, command)

                    output_path = Path(tmp_dir) / f"edited_{uploaded.name}"
                    generate_pdf(edited_document, str(output_path))

                    st.success(f"Applied command: {command.to_dict()}")
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
