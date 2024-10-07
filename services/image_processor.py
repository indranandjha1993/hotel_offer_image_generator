import os
import logging
import time
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

from configs.config import Config
from models import TextStyle


class ImageProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._ensure_folders_exist()
        self.current_time = time.time()

    def _ensure_folders_exist(self) -> None:
        """Ensure that the IMAGES_FOLDER and FONTS_FOLDER exist."""
        os.makedirs(Config.IMAGES_FOLDER, exist_ok=True)
        os.makedirs(Config.FONTS_FOLDER, exist_ok=True)

    def get_font(self, font_name: str, size: int) -> ImageFont.FreeTypeFont:
        """
        Get the specified font or return a default font if not found.

        Args:
            font_name (str): Name of the font file.
            size (int): Font size.

        Returns:
            ImageFont.FreeTypeFont: The font object.
        """
        font_path = os.path.join(Config.FONTS_FOLDER, font_name)
        try:
            return ImageFont.truetype(font_path, size)
        except IOError:
            self.logger.warning(f"Font {font_name} not found. Using default font.")
            return ImageFont.load_default().font_variant(size=size)

    def calculate_text_position(self, text_size: Tuple[int, int], image_size: Tuple[int, int], style: TextStyle) -> \
            Tuple[int, int]:
        """
        Calculate the position of the text on the image.

        Args:
            text_size (Tuple[int, int]): Width and height of the text.
            image_size (Tuple[int, int]): Width and height of the image.
            style (TextStyle): Style information including position.

        Returns:
            Tuple[int, int]: The x and y coordinates for the text.
        """
        position_func = Config.TEXT_POSITIONS.get(style.position, lambda *args: (0, 0))
        return position_func(text_size[0], text_size[1], image_size[0], image_size[1])

    def overlay_text_on_image(self, image: Image.Image, text: str, style: TextStyle) -> Image.Image:
        """
        Overlay text on the given image.

        Args:
            image (Image.Image): The base image.
            text (str): The text to overlay.
            style (TextStyle): Style information for the text.

        Returns:
            Image.Image: The image with overlaid text.
        """
        try:
            draw = ImageDraw.Draw(image, 'RGBA')
            font = self.get_font(style.font_name, style.font_size)

            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            padding = max(5, int(style.font_size * 0.2))
            text_position = self.calculate_text_position((text_width, text_height), image.size, style)

            # Calculate background rectangle
            bg_left = max(0, text_position[0] - padding)
            bg_top = max(0, text_position[1] - padding)
            bg_right = min(image.width, text_position[0] + text_width + padding)
            bg_bottom = min(image.height, text_position[1] + text_height + padding)

            # Draw background
            bg_color_with_opacity = style.bg_color + (int(style.bg_opacity * 255),)
            draw.rectangle((bg_left, bg_top, bg_right, bg_bottom), fill=bg_color_with_opacity)

            # Draw text
            draw.text(text_position, text, font=font, fill=style.text_color)

            return image
        except Exception as e:
            self.logger.error(f"Error in overlaying text: {str(e)}")
            return image

    def save_image(self, image: Image.Image, filename: str) -> None:
        """
        Save the image to the IMAGES_FOLDER.

        Args:
            image (Image.Image): The image to save.
            filename (str): The filename for the image.
        """
        try:
            filepath = os.path.join(Config.IMAGES_FOLDER, filename)
            image.save(filepath)
            self.logger.info(f"Image saved as: {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving image: {str(e)}")

    def get_timestamp_filename(self, filename: str) -> str:
        """
        Get concatenated filename with timestamp

        :param filename:
        :return:
        """
        return f"{int(self.current_time)}_{filename[:50]}"
