from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal, Optional

BlockType = Literal["title", "paragraph", "table", "unknown"]


@dataclass
class LayoutMetadata:
    bbox: tuple[float, float, float, float]
    page_width: float
    page_height: float


@dataclass
class Block:
    id: str
    type: BlockType = "paragraph"
    text: str = ""
    page: int = 1
    layout: Optional[LayoutMetadata] = None


@dataclass
class Page:
    number: int
    width: float
    height: float
    block_ids: list[str] = field(default_factory=list)


@dataclass
class ParsedDocument:
    file_name: str
    pages: list[Page] = field(default_factory=list)
    blocks: list[Block] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "file_name": self.file_name,
            "pages": [asdict(page) for page in self.pages],
            "blocks": [asdict(block) for block in self.blocks],
        }

    def to_markdown(self) -> str:
        lines: list[str] = [f"# {self.file_name}"]
        for page in self.pages:
            lines.append(f"\n## Page {page.number}")
            page_blocks = [block for block in self.blocks if block.page == page.number]
            for block in page_blocks:
                if block.type == "title":
                    lines.append(f"\n### ({block.id}) {block.text}")
                else:
                    lines.append(f"\n[{block.id}] {block.text}")
        return "\n".join(lines)


@dataclass
class EditCommand:
    action: Literal["replace", "rewrite"]
    target: Optional[str] = None
    find: Optional[str] = None
    replace: Optional[str] = None
    style: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)
