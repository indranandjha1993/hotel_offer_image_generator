import os
import time
from config import Config
from models import TextStyle
from services.text_generator import TextGenerator
from services.image_generator import ImageGenerator
from services.image_processor import ImageProcessor
from utils.user_input import get_user_choice


def main():
    try:
        # Initialize services
        text_generator = TextGenerator()
        image_generator = ImageGenerator()

        # Get user inputs
        prompt = input("Enter the hotel offer prompt (default: 'Luxurious beach resort'): ") or "Luxurious beach resort"
        word_limit = int(
            input(f"Enter word limit (default: {Config.DEFAULT_WORD_LIMIT}): ") or Config.DEFAULT_WORD_LIMIT)

        # Generate image and text
        initial_image = image_generator.generate_image(prompt)
        ImageProcessor.save_image(initial_image, f"generated_image_{time.time()}.png")

        offer_text = text_generator.generate_offer_text(prompt, word_limit)
        print(f"Generated offer text: {offer_text}")

        # Get user preferences for text overlay
        style = TextStyle(
            font_name=get_user_choice("Choose a font:", os.listdir(Config.FONTS_FOLDER), Config.DEFAULT_FONT),
            font_size=int(get_user_choice("Choose font size:", [str(size) for size in Config.FONT_SIZES],
                                          str(Config.DEFAULT_FONT_SIZE))),
            position=get_user_choice("Choose text position:", list(Config.TEXT_POSITIONS.keys()),
                                     Config.DEFAULT_TEXT_POSITION),
            text_color=Config.TEXT_COLORS[
                get_user_choice("Choose text color:", list(Config.TEXT_COLORS.keys()), Config.DEFAULT_TEXT_COLOR)],
            bg_color=Config.BACKGROUND_COLORS[
                get_user_choice("Choose background color:", list(Config.BACKGROUND_COLORS.keys()),
                                Config.DEFAULT_BG_COLOR)],
            bg_opacity=float(input(
                f"Enter background opacity (0.0 to 1.0, default: {Config.DEFAULT_BG_OPACITY}): ") or Config.DEFAULT_BG_OPACITY)
        )

        # Apply text overlay and save final image
        final_image = ImageProcessor.overlay_text_on_image(initial_image.copy(), offer_text, style)
        ImageProcessor.save_image(final_image, f"final_offer_image_{time.time()}.png")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
