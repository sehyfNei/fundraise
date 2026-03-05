from pdf_editor.ui_viewer import build_pdf_overlay_html, encode_pdf_base64


def test_encode_pdf_base64_produces_string():
    data = b"%PDF-1.4\n"
    encoded = encode_pdf_base64(data)
    assert isinstance(encoded, str)
    assert len(encoded) > 0


def test_build_pdf_overlay_html_contains_selected_marker():
    view_model = {
        "pages": [{"number": 1, "width": 600, "height": 800, "block_ids": ["paragraph_1"]}],
        "blocks": [
            {
                "id": "paragraph_1",
                "page": 1,
                "type": "paragraph",
                "text": "hello",
                "bbox": [10, 10, 100, 30],
                "normalized_bbox": {"left": 0.1, "top": 0.1, "width": 0.2, "height": 0.05},
            }
        ],
    }
    html = build_pdf_overlay_html("ZmFrZQ==", view_model, "paragraph_1")
    assert "data:application/pdf;base64,ZmFrZQ==" in html
    assert "selected" in html
    assert "paragraph_1" in html
