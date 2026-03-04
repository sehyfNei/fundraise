# LLM Controlled PDF Editor (MVP)

This project is a practical MVP for an **LLM-controlled PDF editor**.

You upload a PDF, give natural-language instructions, and the system:
1. Parses the PDF into a structured JSON-like model.
2. Converts your instruction into an edit command.
3. Applies the command on the document model.
4. Regenerates an edited PDF.

## How editing works (current MVP)

The app does **model-level editing**, not direct pixel-level PDF manipulation.

- `parse_pdf(...)` extracts text blocks from each page and assigns IDs like `paragraph_1`, `paragraph_2`, etc.
- `interpret_instruction(...)` reads your text command and maps it into an `EditCommand` object.
- `apply_command(...)` updates the in-memory document model:
  - `replace`: global string replacement in every block.
  - `rewrite`: rewrites a single targeted paragraph (currently through a placeholder function).
- `generate_pdf(...)` writes updated text back to a new PDF.

### Supported instruction formats

- `replace all "Company A" with "Company B"`
- `rewrite paragraph 2 in professional tone`
- `rewrite paragraph 1`

## User interface flow

The Streamlit UI is intentionally simple:

1. **Upload PDF**
2. **Preview extracted paragraph IDs** (so you know what can be targeted)
3. **Write instruction** in plain English using supported patterns
4. **Apply instruction**
5. **Download edited PDF**

## MVP Features

- Upload PDF
- Extract page text blocks/paragraphs
- Natural-language command interpretation
- `replace` action (`replace all "A" with "B"`)
- `rewrite` action (`rewrite paragraph 2 in professional tone`)
- Export edited PDF

## Tech Stack

- Python 3.10+
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF parsing
- [ReportLab](https://www.reportlab.com/dev/docs/) for PDF generation
- [Streamlit](https://streamlit.io/) for a quick UI

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- This MVP focuses on text-level edits, not pixel-perfect layout preservation.
- For production-grade layout-aware editing, convert PDF to an intermediate format (HTML/Markdown + layout metadata) and regenerate from that structure.
