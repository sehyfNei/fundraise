from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ReaderAction:
    """
    Command payload expected from a PDF.js-like frontend.

    selected_block_id allows click-to-edit box interactions.
    instruction holds natural-language command from user.
    """

    instruction: str
    selected_block_id: Optional[str] = None
