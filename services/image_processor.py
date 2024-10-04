import os

from PIL import Image, ImageDraw, ImageFont
from models import TextStyle
from config import Config


class ImageProcessor:
    @staticmethod
    def get_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
        font_path = os.path.join(Config.FONTS_FOLDER, font_name)
        try:
            return ImageFont.truetype(font_path, size)
        except IOError:
            print(f"Font {font_name} not found. Using default font.")
            return ImageFont.load_default().font_variant(size=size)

    @staticmethod
    def overlay_text_on_image(image: Image.Image, text: str, style: TextStyle) -> Image.Image:
        try:
            draw = ImageDraw.Draw(image, 'RGBA')
            font = ImageProcessor.get_font(style.font_name, style.font_size)

            image_width, image_height = image.size

            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            padding = max(5, int(style.font_size * 0.2))

            position_func = Config.TEXT_POSITIONS[style.position]
            text_position = position_func(text_width, text_height, image_width, image_height)

            bg_left = max(0, text_position[0] - padding)
            bg_top = max(0, text_position[1] - padding)
            bg_right = min(image_width, text_position[0] + text_width + padding)
            bg_bottom = min(image_height, text_position[1] + text_height + padding)

            bg_color_with_opacity = style.bg_color + (int(style.bg_opacity * 255),)
            background_bbox = (bg_left, bg_top, bg_right, bg_bottom)
            draw.rectangle(background_bbox, fill=bg_color_with_opacity)

            draw.text(text_position, text, font=font, fill=style.text_color)

            return image
        except Exception as e:
            print(f"Error in overlaying text: {str(e)}")
            return image

    @staticmethod
    def save_image(image: Image.Image, filename: str) -> None:
        filepath = os.path.join(Config.IMAGES_FOLDER, filename)
        image.save(filepath)
        print(f"Image saved as: {filepath}")
