from dataclasses import dataclass
from typing import Tuple


@dataclass
class TextStyle:
    font_name: str
    font_size: int
    position: str
    text_color: Tuple[int, int, int]
    bg_color: Tuple[int, int, int]
    bg_opacity: float
