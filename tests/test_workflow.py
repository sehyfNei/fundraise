from pdf_editor.models import EditCommand
from pdf_editor.workflow import inject_selected_target


def test_inject_selected_target_for_rewrite_without_target():
    cmd = EditCommand(action="rewrite", style="professional")
    updated = inject_selected_target(cmd, "page_1_block_2")
    assert updated.target == "page_1_block_2"


def test_inject_selected_target_does_not_override_explicit_target():
    cmd = EditCommand(action="rewrite", target="paragraph_1", style="professional")
    updated = inject_selected_target(cmd, "page_1_block_2")
    assert updated.target == "paragraph_1"
