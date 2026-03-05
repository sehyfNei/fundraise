from pdf_editor.models import Block, LayoutMetadata, Page, ParsedDocument
from pdf_editor.view_model import to_reader_view_model


def test_reader_view_model_contains_normalized_bbox():
    doc = ParsedDocument(
        file_name="sample.pdf",
        pages=[Page(number=1, width=200, height=400, block_ids=["b1"])],
        blocks=[
            Block(
                id="b1",
                type="paragraph",
                text="Hello",
                page=1,
                layout=LayoutMetadata(bbox=(20, 40, 120, 140), page_width=200, page_height=400),
            )
        ],
    )

    vm = to_reader_view_model(doc)
    assert vm["file_name"] == "sample.pdf"
    assert vm["pages"][0]["number"] == 1
    nb = vm["blocks"][0]["normalized_bbox"]
    assert nb == {"left": 0.1, "top": 0.1, "width": 0.5, "height": 0.25}


def test_reader_view_model_handles_missing_layout():
    doc = ParsedDocument(
        file_name="sample.pdf",
        pages=[Page(number=1, width=200, height=400, block_ids=["b1"])],
        blocks=[Block(id="b1", type="paragraph", text="No layout", page=1)],
    )

    vm = to_reader_view_model(doc)
    assert vm["blocks"][0]["normalized_bbox"] is None
