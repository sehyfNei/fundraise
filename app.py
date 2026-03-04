from __future__ import annotations

import os
import tempfile
from pathlib import Path

import streamlit as st

from pdf_editor.editor import apply_command
from pdf_editor.generator import generate_pdf
from pdf_editor.interpreter import InstructionParseError, interpret_instruction
from pdf_editor.parser import parse_pdf
from pdf_editor.workflow import inject_selected_target


def _ui_build_label() -> str:
    """Expose a visible build/version marker to avoid confusion with stale UI sessions."""
    return os.getenv("PDF_EDITOR_UI_VERSION", "v2-box-targeted")


st.set_page_config(page_title="LLM PDF Editor MVP", layout="wide")
st.title("LLM Controlled PDF Editor")
st.caption("Layout-aware pipeline: PDF → Markdown + layout metadata → edit → regenerate PDF")
st.info(f"UI build: {_ui_build_label()}")

with st.sidebar:
    st.subheader("How to use")
    st.caption(f"Build: {_ui_build_label()}")
    if st.button("Force refresh app state"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    st.markdown(
        """
1. Upload a PDF.
2. Pick a block (box) from the selector.
3. Enter an instruction.
4. Click **Apply instruction**.
5. Download the edited PDF.

**Supported examples**
- `replace all "Company A" with "Company B"`
- `rewrite paragraph 2 in professional tone`
- `rewrite selected block in professional tone`
        """
    )

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
instruction = st.text_input("Instruction", placeholder='e.g. rewrite selected block in professional tone')

if uploaded is not None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = Path(tmp_dir) / uploaded.name
        input_path.write_bytes(uploaded.read())

        document = parse_pdf(str(input_path), uploaded.name)

        st.subheader("Intermediate representation")
        tab_md, tab_boxes, tab_debug = st.tabs(["Markdown", "Boxes", "Layout metadata"])

        with tab_md:
            st.code(document.to_markdown(), language="markdown")

        with tab_boxes:
            if document.blocks:
                box_rows = []
                for b in document.blocks:
                    bbox = b.layout.bbox if b.layout else None
                    box_rows.append(
                        {
                            "id": b.id,
                            "page": b.page,
                            "type": b.type,
                            "bbox": str(bbox),
                            "preview": b.text[:120],
                        }
                    )
                st.table(box_rows)
                selected_block_id = st.selectbox(
                    "Select box to target for 'rewrite selected block'",
                    options=[b.id for b in document.blocks],
                )
            else:
                st.info("No editable blocks detected in this PDF.")
                selected_block_id = None

        with tab_debug:
            st.json(document.to_dict())

        if st.button("Apply instruction"):
            if not instruction.strip():
                st.warning("Please provide an instruction")
            else:
                try:
                    command = interpret_instruction(instruction)
                    command = inject_selected_target(command, selected_block_id)
                    st.info(f"Interpreted command: {command.to_dict()}")

                    edited_document = apply_command(document, command)

                    output_path = Path(tmp_dir) / f"edited_{uploaded.name}"
                    generate_pdf(edited_document, str(output_path))

                    st.success("Edit applied and regenerated with layout metadata.")
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
