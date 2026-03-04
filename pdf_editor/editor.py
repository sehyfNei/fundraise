from __future__ import annotations

from pdf_editor.llm import rewrite_text_with_llm
from pdf_editor.models import EditCommand, ParsedDocument


def apply_command(document: ParsedDocument, command: EditCommand) -> ParsedDocument:
    if command.action == "replace":
        if command.find is None or command.replace is None:
            raise ValueError("Replace command must include find and replace text")
        for block in document.blocks:
            block.text = block.text.replace(command.find, command.replace)
        return document

    if command.action == "rewrite":
        if command.target is None:
            raise ValueError("Rewrite command must include a target")
        for block in document.blocks:
            if block.id == command.target:
                block.text = rewrite_text_with_llm(block.text, command.style)
                return document
        raise ValueError(f"Target not found: {command.target}")

    raise ValueError(f"Unsupported action: {command.action}")
