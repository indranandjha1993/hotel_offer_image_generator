import os
from dotenv import load_dotenv
from typing import Tuple, Callable, Dict, List

load_dotenv()

# Type aliases
Position = Tuple[int, int]
Color = Tuple[int, int, int]
PositionFunction = Callable[[int, int, int, int], Position]


class Config:
    IMAGES_FOLDER = "images"
    FONTS_FOLDER = "fonts"
    DEFAULT_FONT = "arial.ttf"
    DEFAULT_FONT_SIZE = 32
    DEFAULT_TEXT_POSITION = "center"
    DEFAULT_TEXT_COLOR = "white"
    DEFAULT_BG_COLOR = "black"
    DEFAULT_BG_OPACITY = 0.5
    DEFAULT_WORD_LIMIT = 5

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    TEXT_POSITIONS: Dict[str, PositionFunction] = {
        "top-left": lambda text_w, text_h, w, h: (10, 10),
        "top-center": lambda text_w, text_h, w, h: ((w - text_w) // 2, 10),
        "top-right": lambda text_w, text_h, w, h: (w - text_w - 10, 10),
        "center-left": lambda text_w, text_h, w, h: (10, (h - text_h) // 2),
        "center": lambda text_w, text_h, w, h: ((w - text_w) // 2, (h - text_h) // 2),
        "center-right": lambda text_w, text_h, w, h: (w - text_w - 10, (h - text_h) // 2),
        "bottom-left": lambda text_w, text_h, w, h: (10, h - text_h - 10),
        "bottom-center": lambda text_w, text_h, w, h: ((w - text_w) // 2, h - text_h - 10),
        "bottom-right": lambda text_w, text_h, w, h: (w - text_w - 10, h - text_h - 10),
        "middle-top-left": lambda text_w, text_h, w, h: (w // 4 - text_w // 2, h // 4 - text_h // 2),
        "middle-top-right": lambda text_w, text_h, w, h: (3 * w // 4 - text_w // 2, h // 4 - text_h // 2),
        "middle-bottom-left": lambda text_w, text_h, w, h: (w // 4 - text_w // 2, 3 * h // 4 - text_h // 2),
        "middle-bottom-right": lambda text_w, text_h, w, h: (3 * w // 4 - text_w // 2, 3 * h // 4 - text_h // 2),
    }

    TEXT_COLORS: Dict[str, Color] = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0)
    }

    BACKGROUND_COLORS = TEXT_COLORS.copy()

    FONT_SIZES = [12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72]
