from __future__ import annotations

import fitz

from pdf_editor.models import Block, LayoutMetadata, Page, ParsedDocument


def _classify_block(text: str) -> str:
    clean = text.strip()
    if not clean:
        return "unknown"
    if len(clean) < 90 and clean.isupper():
        return "title"
    return "paragraph"


def parse_pdf(path: str, file_name: str) -> ParsedDocument:
    doc = fitz.open(path)
    blocks: list[Block] = []
    pages: list[Page] = []
    paragraph_index = 0

    try:
        for page_idx, page in enumerate(doc, start=1):
            rect = page.rect
            page_model = Page(number=page_idx, width=rect.width, height=rect.height)
            page_blocks = page.get_text("blocks")

            for raw in page_blocks:
                x0, y0, x1, y1, text, *_ = raw
                text = text.strip()
                if not text:
                    continue

                block_type = _classify_block(text)
                if block_type == "paragraph":
                    paragraph_index += 1
                    block_id = f"paragraph_{paragraph_index}"
                else:
                    block_id = f"page_{page_idx}_block_{len(blocks) + 1}"

                blocks.append(
                    Block(
                        id=block_id,
                        type=block_type,
                        text=text,
                        page=page_idx,
                        layout=LayoutMetadata(
                            bbox=(x0, y0, x1, y1),
                            page_width=rect.width,
                            page_height=rect.height,
                        ),
                    )
                )
                page_model.block_ids.append(block_id)

            pages.append(page_model)
    finally:
        doc.close()

    return ParsedDocument(file_name=file_name, pages=pages, blocks=blocks)
