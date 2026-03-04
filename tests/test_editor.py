from pdf_editor.editor import apply_command
from pdf_editor.models import Block, EditCommand, ParsedDocument


def test_replace_command_applies_globally():
    doc = ParsedDocument(
        file_name="x.pdf",
        blocks=[
            Block(id="paragraph_1", type="paragraph", text="AI helps", page=1),
            Block(id="paragraph_2", type="paragraph", text="AI scales", page=1),
        ],
    )

    cmd = EditCommand(action="replace", find="AI", replace="Artificial Intelligence")
    edited = apply_command(doc, cmd)
    assert edited.blocks[0].text == "Artificial Intelligence helps"
    assert edited.blocks[1].text == "Artificial Intelligence scales"


def test_rewrite_command_updates_target_block():
    doc = ParsedDocument(
        file_name="x.pdf",
        blocks=[Block(id="paragraph_1", type="paragraph", text="raw draft", page=1)],
    )

    cmd = EditCommand(action="rewrite", target="paragraph_1", style="professional")
    edited = apply_command(doc, cmd)
    assert edited.blocks[0].text.startswith("[professional rewrite]")
