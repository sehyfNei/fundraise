from pdf_editor.models import Block, LayoutMetadata, Page, ParsedDocument


def test_document_to_markdown_includes_pages_and_ids():
    doc = ParsedDocument(
        file_name="sample.pdf",
        pages=[Page(number=1, width=612, height=792, block_ids=["paragraph_1"])],
        blocks=[
            Block(
                id="paragraph_1",
                type="paragraph",
                text="Hello world",
                page=1,
                layout=LayoutMetadata(bbox=(10, 10, 100, 40), page_width=612, page_height=792),
            )
        ],
    )

    md = doc.to_markdown()
    assert "# sample.pdf" in md
    assert "## Page 1" in md
    assert "[paragraph_1] Hello world" in md
