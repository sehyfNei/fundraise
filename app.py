from __future__ import annotations

import os
import tempfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from pdf_editor.editor import apply_command
from pdf_editor.generator import generate_pdf
from pdf_editor.interpreter import InstructionParseError, interpret_instruction
from pdf_editor.parser import parse_pdf
from pdf_editor.ui_viewer import build_pdf_overlay_html, encode_pdf_base64
from pdf_editor.view_model import to_reader_view_model
from pdf_editor.workflow import inject_selected_target


def _ui_build_label() -> str:
    return os.getenv("PDF_EDITOR_UI_VERSION", "v3-canvas-view")


st.set_page_config(page_title="LLM PDF Editor", layout="wide")
st.title("AI PDF Editor")
st.caption("Canva-like editing view: original PDF with component boxes.")
st.caption(f"Build: {_ui_build_label()}")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded is None:
    st.info("Upload a PDF to start editing.")
    st.stop()

with tempfile.TemporaryDirectory() as tmp_dir:
    input_path = Path(tmp_dir) / uploaded.name
    input_path.write_bytes(uploaded.read())

    document = parse_pdf(str(input_path), uploaded.name)
    reader_vm = to_reader_view_model(document)

    col_view, col_actions = st.columns([2.2, 1.0])

    with col_view:
        st.subheader("Document canvas")
        selected_block_id = st.session_state.get("selected_block_id")
        if selected_block_id not in [b.id for b in document.blocks]:
            selected_block_id = document.blocks[0].id if document.blocks else None

        pdf_b64 = encode_pdf_base64(input_path.read_bytes())
        viewer_html = build_pdf_overlay_html(pdf_b64, reader_vm, selected_block_id)
        components.html(viewer_html, height=920, scrolling=False)

    with col_actions:
        st.subheader("Edit")
        st.selectbox(
            "Selected component",
            options=[b.id for b in document.blocks] if document.blocks else [],
            key="selected_block_id",
            help="Use this to target a specific box on the canvas.",
        )

        instruction = st.text_area(
            "Instruction",
            placeholder='e.g. rewrite selected block in professional tone',
            height=100,
        )

        st.caption("Examples")
        st.write('- `rewrite selected block in professional tone`')
        st.write('- `replace all "Company A" with "Company B"`')

        if st.button("Apply edit", type="primary", use_container_width=True):
            if not instruction.strip():
                st.warning("Please provide an instruction")
            else:
                try:
                    command = interpret_instruction(instruction)
                    command = inject_selected_target(command, st.session_state.get("selected_block_id"))
                    edited_document = apply_command(document, command)

                    output_path = Path(tmp_dir) / f"edited_{uploaded.name}"
                    generate_pdf(edited_document, str(output_path))

                    st.success("Edit applied.")
                    st.download_button(
                        "Download edited PDF",
                        data=output_path.read_bytes(),
                        file_name=output_path.name,
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except InstructionParseError as err:
                    st.error(str(err))
                except Exception as err:  # noqa: BLE001
                    st.error(f"Failed to apply edit: {err}")

        with st.expander("Show component list"):
            st.table(
                [
                    {
                        "id": b.id,
                        "page": b.page,
                        "type": b.type,
                        "preview": b.text[:80],
                    }
                    for b in document.blocks
                ]
            )
