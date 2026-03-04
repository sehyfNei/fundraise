from __future__ import annotations

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from pdf_editor.models import ParsedDocument


def generate_pdf(document: ParsedDocument, output_path: str) -> str:
    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER

    y = height - 50
    for block in document.blocks:
        lines = _wrap_text(block.text, max_chars=95)
        for line in lines:
            c.drawString(50, y, line)
            y -= 16
            if y < 50:
                c.showPage()
                y = height - 50
        y -= 6

    c.save()
    return output_path


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
