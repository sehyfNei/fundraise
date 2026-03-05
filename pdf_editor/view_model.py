from __future__ import annotations

from pdf_editor.models import ParsedDocument


def to_reader_view_model(document: ParsedDocument) -> dict:
    """
    Build a frontend-oriented model for PDF.js style viewers.

    The frontend can draw clickable overlays using normalized coordinates
    independent of zoom.
    """
    pages = [
        {
            "number": page.number,
            "width": page.width,
            "height": page.height,
            "block_ids": page.block_ids,
        }
        for page in document.pages
    ]

    blocks: list[dict] = []
    for block in document.blocks:
        bbox = block.layout.bbox if block.layout else None
        page_w = block.layout.page_width if block.layout else None
        page_h = block.layout.page_height if block.layout else None
        blocks.append(
            {
                "id": block.id,
                "page": block.page,
                "type": block.type,
                "text": block.text,
                "bbox": list(bbox) if bbox else None,
                "normalized_bbox": _normalize_bbox(bbox, page_w, page_h),
            }
        )

    return {
        "file_name": document.file_name,
        "pages": pages,
        "blocks": blocks,
    }


def _normalize_bbox(
    bbox: tuple[float, float, float, float] | None,
    page_width: float | None,
    page_height: float | None,
) -> dict | None:
    if not bbox or not page_width or not page_height:
        return None

    x0, y0, x1, y1 = bbox
    return {
        "left": x0 / page_width,
        "top": y0 / page_height,
        "width": max(0.0, (x1 - x0) / page_width),
        "height": max(0.0, (y1 - y0) / page_height),
    }
