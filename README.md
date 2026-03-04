# LLM Controlled PDF Editor (Layout-Aware MVP)

This project is an MVP for an **LLM-controlled PDF editor** that uses an intermediate representation.

Pipeline:
1. Parse PDF into **Markdown-like content + layout metadata**.
2. Interpret user instruction into a structured edit command.
3. Apply edit on the intermediate representation.
4. Regenerate PDF using original layout metadata.

## Why this approach

Directly editing raw PDF bytes is brittle.
This project follows a production-style direction:

- **PDF → intermediate representation** (`ParsedDocument` with pages, blocks, and bbox metadata)
- Edit at structured content level
- Regenerate from structure while preserving approximate original layout

## How editing works

- `parse_pdf(...)` extracts text blocks and stores:
  - `block.id` (e.g., `paragraph_1`)
  - `block.text`
  - `layout.bbox`, `layout.page_width`, `layout.page_height`
- `interpret_instruction(...)` converts NL instruction into `EditCommand`
- `apply_command(...)` edits block text in the intermediate representation
- `generate_pdf(...)` redraws each block near its original coordinates

## Supported instruction formats

- `replace all "Company A" with "Company B"`
- `rewrite paragraph 2 in professional tone`
- `rewrite paragraph 1`

## User interface

Streamlit UI includes:

- **Markdown tab**: editable-source style preview of parsed document
- **Paragraph IDs tab**: target IDs for rewrite commands
- **Layout metadata tab**: raw structured JSON for debugging
- Command interpretation feedback before apply
- Download regenerated PDF

## Tech Stack

- Python 3.10+
- [PyMuPDF](https://pymupdf.readthedocs.io/) for parsing
- [ReportLab](https://www.reportlab.com/dev/docs/) for regeneration
- [Streamlit](https://streamlit.io/) for UI

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Current limitations

- Layout is **approximately preserved**, not pixel-perfect.
- Tables/images are not yet reconstructed semantically.
- Rewrite currently uses a placeholder function (`llm.py`) and should be replaced with a real LLM backend.
