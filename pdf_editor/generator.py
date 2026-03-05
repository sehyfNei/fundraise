from __future__ import annotations

from reportlab.pdfgen import canvas

from pdf_editor.models import ParsedDocument


def generate_pdf(document: ParsedDocument, output_path: str) -> str:
    """
    Regenerate PDF from intermediate representation (markdown-equivalent blocks + layout metadata).
    """
    if not document.pages:
        c = canvas.Canvas(output_path)
        c.save()
        return output_path

    first_page = document.pages[0]
    c = canvas.Canvas(output_path, pagesize=(first_page.width, first_page.height))

    for idx, page in enumerate(document.pages):
        if idx > 0:
            c.setPageSize((page.width, page.height))
            c.showPage()

        page_blocks = [block for block in document.blocks if block.page == page.number]
        for block in page_blocks:
            _draw_block(c, block.text, block.layout.bbox if block.layout else None, page.height)

    c.save()
    return output_path


def _draw_block(c: canvas.Canvas, text: str, bbox: tuple[float, float, float, float] | None, page_height: float) -> None:
    if not bbox:
        return

    x0, y0, x1, _ = bbox
    max_chars = max(20, int((x1 - x0) / 6.5))
    lines = _wrap_text(text, max_chars=max_chars)

    # PDF parser coordinates start top-left for y; reportlab uses bottom-left.
    draw_y = page_height - y0
    for line in lines:
        c.drawString(x0, draw_y, line)
        draw_y -= 14


def _wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []

    for word in words:
        trial = " ".join(current + [word])
        if len(trial) <= max_chars:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))

    return lines if lines else [""]
