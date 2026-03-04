from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal, Optional

BlockType = Literal["title", "paragraph", "table", "unknown"]


@dataclass
class Block:
    id: str
    type: BlockType = "paragraph"
    text: str = ""
    page: int = 1
    bbox: Optional[tuple[float, float, float, float]] = None


@dataclass
class ParsedDocument:
    file_name: str
    blocks: list[Block] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"file_name": self.file_name, "blocks": [asdict(block) for block in self.blocks]}


@dataclass
class EditCommand:
    action: Literal["replace", "rewrite"]
    target: Optional[str] = None
    find: Optional[str] = None
    replace: Optional[str] = None
    style: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)
