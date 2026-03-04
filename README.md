# LLM Controlled PDF Editor (Layout-Aware MVP)

This project is an MVP for an **LLM-controlled PDF editor** that uses an intermediate representation.

Pipeline:
1. Parse PDF into **Markdown-like content + layout metadata**.
2. Interpret user instruction into a structured edit command.
3. Apply edit on the intermediate representation.
4. Regenerate PDF using original layout metadata.

## Canva/Adobe-like direction (implemented MVP path)

This version adds a **box-targeted editing flow**:

- PDF is parsed into editable blocks (`id`, `type`, `bbox`, `page`).
- UI shows all boxes and lets you select one.
- You can run: `rewrite selected block in professional tone`.
- The selected box ID is injected into the rewrite command and updated.

This is the backend foundation required before integrating a full browser PDF canvas.

## Mozilla PDF.js integration plan

To get closer to Canva/Adobe UX:

1. Use PDF.js viewer to render PDF pages in-browser.
2. Draw overlay rectangles using parser `bbox` metadata.
3. Click a rectangle to set `selected_block_id`.
4. Send instruction + selected ID to backend.
5. Regenerate and hot-reload edited PDF.

The current project already supports steps 3–5 on the backend side.

## How editing works

- `parse_pdf(...)` extracts text blocks and stores:
  - `block.id` (e.g., `paragraph_1`)
  - `block.text`
  - `layout.bbox`, `layout.page_width`, `layout.page_height`
- `interpret_instruction(...)` converts NL instruction into `EditCommand`
- `inject_selected_target(...)` maps selected UI box to rewrite command
- `apply_command(...)` edits block text in the intermediate representation
- `generate_pdf(...)` redraws each block near its original coordinates

## Supported instruction formats

- `replace all "Company A" with "Company B"`
- `rewrite paragraph 2 in professional tone`
- `rewrite selected block in professional tone`

## User interface

Streamlit UI includes:

- **Markdown tab**: parsed document projection
- **Boxes tab**: block IDs, bounding boxes, and selectable target block
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


## Frontend showing older version?

If you still see an older UI, check these quickly:

1. Restart Streamlit process (`Ctrl+C` then `streamlit run app.py`).
2. Use sidebar button **Force refresh app state**.
3. Confirm the on-screen build label at top: `UI build: v2-box-targeted` (or set `PDF_EDITOR_UI_VERSION`).
4. Ensure you are launching from this repo path and branch.

You can also override build label:

```bash
PDF_EDITOR_UI_VERSION=my-local-build streamlit run app.py
```


## Build a real PDF Reader editing UX (Canva/Adobe style)

To make this feel like Adobe/Canva, use a browser PDF viewer (PDF.js) and wire it to this backend.

### 1) Reader rendering layer
- Render PDF pages with Mozilla PDF.js.
- Keep a separate HTML overlay layer per page for interaction boxes.

### 2) Overlay box model (already supported by backend)
- Use `pdf_editor.view_model.to_reader_view_model(...)` to get blocks with:
  - `id`
  - `page`
  - `bbox`
  - `normalized_bbox` (0..1 coords for zoom-safe overlay rendering)
- Draw each box using `normalized_bbox` relative to page viewport size.

### 3) Click-to-edit interaction
- On box click, store `selected_block_id` in frontend state.
- Send payload like:

```json
{
  "instruction": "rewrite selected block in professional tone",
  "selected_block_id": "paragraph_5"
}
```

- Backend flow:
  1. `interpret_instruction(instruction)`
  2. `inject_selected_target(command, selected_block_id)`
  3. `apply_command(document, command)`
  4. `generate_pdf(document, output_path)`

### 4) Production UX improvements
- Inline text edit mode (double-click box to edit raw text directly).
- Multi-select block edits (style/tone transform on selected set).
- Undo/redo stack (command history).
- Version snapshots for safe rollback.
- Background OCR fallback for scanned PDFs.

This repo now contains the core data contract and command pipeline needed for that PDF.js UI.
