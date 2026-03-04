from __future__ import annotations

from pdf_editor.models import EditCommand


def inject_selected_target(command: EditCommand, selected_block_id: str | None) -> EditCommand:
    """
    If user chose a block in UI and command is rewrite without explicit target,
    bind the command to that selected block.
    """
    if command.action == "rewrite" and command.target is None and selected_block_id:
        command.target = selected_block_id
    return command
