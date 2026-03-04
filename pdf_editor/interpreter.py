from __future__ import annotations

import re

from pdf_editor.models import EditCommand


class InstructionParseError(ValueError):
    pass


def interpret_instruction(instruction: str) -> EditCommand:
    text = instruction.strip()

    replace_pattern = re.compile(
        r'replace(?:\s+all)?\s+"(?P<find>.+?)"\s+with\s+"(?P<replace>.+?)"',
        flags=re.IGNORECASE,
    )
    match = replace_pattern.search(text)
    if match:
        return EditCommand(
            action="replace",
            find=match.group("find"),
            replace=match.group("replace"),
        )

    rewrite_pattern = re.compile(
        r"rewrite\s+paragraph\s+(?P<idx>\d+)(?:\s+in\s+(?P<style>.+?)\s+tone)?$",
        flags=re.IGNORECASE,
    )
    match = rewrite_pattern.search(text)
    if match:
        idx = match.group("idx")
        style = match.group("style")
        return EditCommand(action="rewrite", target=f"paragraph_{idx}", style=style)

    raise InstructionParseError(
        "Instruction not recognized. Try: replace all \"A\" with \"B\" or rewrite paragraph 2 in professional tone"
    )
