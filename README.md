# LLM Controlled PDF Editor (MVP)

This project is a practical MVP for an **LLM-controlled PDF editor**.

You upload a PDF, give natural-language instructions, and the system:
1. Parses the PDF into a structured JSON-like model.
2. Converts your instruction into an edit command.
3. Applies the command on the document model.
4. Regenerates an edited PDF.

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

## Example Instructions

- `replace all "Company A" with "Company B"`
- `rewrite paragraph 2 in professional tone`
- `rewrite paragraph 1`

## Notes

- This MVP focuses on text-level edits, not pixel-perfect layout preservation.
- For production-grade layout-aware editing, convert PDF to an intermediate format (HTML/Markdown + layout metadata) and regenerate from that structure.
