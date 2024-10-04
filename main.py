import os
import time
from io import BytesIO
from typing import Tuple, Callable, Dict, List

import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Constants
IMAGES_FOLDER = "images"
FONTS_FOLDER = "fonts"
DEFAULT_FONT = "arial.ttf"
DEFAULT_FONT_SIZE = 32
DEFAULT_TEXT_POSITION = "center"
DEFAULT_TEXT_COLOR = "white"
DEFAULT_BG_COLOR = "black"
DEFAULT_BG_OPACITY = 0.5
DEFAULT_WORD_LIMIT = 5

# Ensure necessary folders exist
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(FONTS_FOLDER, exist_ok=True)

# Type aliases
Position = Tuple[int, int]
Color = Tuple[int, int, int]
PositionFunction = Callable[[int, int, int, int], Position]

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

BACKGROUND_COLORS: Dict[str, Color] = TEXT_COLORS.copy()

FONT_SIZES: List[int] = [12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72]


def generate_offer_text(prompt: str, word_limit: int) -> str:
    """Generate offer text using OpenAI's GPT model."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates short, catchy hotel offers."},
                {"role": "user",
                 "content": f"Generate a short, catchy hotel offer based on the following prompt: {prompt}. The offer should be approximately {word_limit} words long."}
            ],
            max_tokens=100
        )
        return completion.choices[0].message.content.strip().replace('"', '')
    except Exception as e:
        print(f"Error in generating offer text: {str(e)}")
        return f"Special offer for {prompt}!"


def generate_image(prompt: str) -> Image.Image:
    """Generate an image using DALL-E model."""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A high-quality, professional hotel promotional image based on: {prompt}. The image must not contain any text, words, or letters.",
            size="1792x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        return Image.open(BytesIO(image_response.content))
    except Exception as e:
        print(f"Error in generating image: {str(e)}")
        return Image.new('RGB', (1024, 1024), color='white')


def get_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    """Get font object based on name and size."""
    font_path = os.path.join(FONTS_FOLDER, font_name)
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        print(f"Font {font_name} not found. Using default font.")
        return ImageFont.load_default().font_variant(size=size)


def overlay_text_on_image(
        image: Image.Image,
        text: str,
        font_name: str,
        font_size: int,
        position: str,
        text_color: Color,
        bg_color: Color,
        bg_opacity: float
) -> Image.Image:
    """Overlay text on the image with customized options."""
    try:
        draw = ImageDraw.Draw(image, 'RGBA')
        font = get_font(font_name, font_size)

        image_width, image_height = image.size

        # Calculate text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Add padding to the text background
        padding = max(5, int(font_size * 0.2))  # Adjust padding based on font size

        # Determine text position
        position_func = TEXT_POSITIONS[position]
        text_position = position_func(text_width, text_height, image_width, image_height)

        # Calculate background position and size
        bg_left = text_position[0] - padding
        bg_top = text_position[1] - padding
        bg_right = text_position[0] + text_width + padding
        bg_bottom = text_position[1] + text_height + padding

        # Ensure background stays within image boundaries
        bg_left = max(0, bg_left)
        bg_top = max(0, bg_top)
        bg_right = min(image_width, bg_right)
        bg_bottom = min(image_height, bg_bottom)

        # Create a semi-transparent background
        bg_color_with_opacity = bg_color + (int(bg_opacity * 255),)
        background_bbox = (bg_left, bg_top, bg_right, bg_bottom)
        draw.rectangle(background_bbox, fill=bg_color_with_opacity)

        # Adjust text position to account for padding
        adjusted_text_position = (text_position[0], text_position[1])

        # Draw text
        draw.text(adjusted_text_position, text, font=font, fill=text_color)

        return image
    except Exception as e:
        print(f"Error in overlaying text: {str(e)}")
        return image


def save_image(image: Image.Image, filename: str) -> None:
    """Save image to the images folder."""
    filepath = os.path.join(IMAGES_FOLDER, filename)
    image.save(filepath)
    print(f"Image saved as: {filepath}")


def get_user_choice(prompt: str, options: List[str], default: str) -> str:
    """Get user choice from a list of options with a default value."""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        choice = input(f"Enter your choice (number) or press Enter for default ({default}): ").strip()
        if choice == "":
            return default
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(options):
                return options[choice_index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or press Enter for default.")


def main():
    try:
        prompt = input("Enter the hotel offer prompt (default: 'Luxurious beach resort'): ") or "Luxurious beach resort"
        word_limit = int(input(f"Enter word limit (default: {DEFAULT_WORD_LIMIT}): ") or DEFAULT_WORD_LIMIT)

        # Generate and save the initial image
        initial_image = generate_image(prompt)
        save_image(initial_image, f"generated_image_{time.time()}.png")

        # Generate offer text
        offer_text = generate_offer_text(prompt, word_limit)
        print(f"Generated offer text: {offer_text}")

        # Get user preferences for text overlay
        font_name = get_user_choice("Choose a font:", os.listdir(FONTS_FOLDER), DEFAULT_FONT)
        font_size = int(
            get_user_choice("Choose font size:", [str(size) for size in FONT_SIZES], str(DEFAULT_FONT_SIZE)))
        text_position = get_user_choice("Choose text position:", list(TEXT_POSITIONS.keys()), DEFAULT_TEXT_POSITION)
        text_color = TEXT_COLORS[get_user_choice("Choose text color:", list(TEXT_COLORS.keys()), DEFAULT_TEXT_COLOR)]
        bg_color = BACKGROUND_COLORS[
            get_user_choice("Choose background color:", list(BACKGROUND_COLORS.keys()), DEFAULT_BG_COLOR)]
        bg_opacity = float(
            input(f"Enter background opacity (0.0 to 1.0, default: {DEFAULT_BG_OPACITY}): ") or DEFAULT_BG_OPACITY)

        # Apply text overlay
        final_image = overlay_text_on_image(
            initial_image.copy(),
            offer_text,
            font_name,
            font_size,
            text_position,
            text_color,
            bg_color,
            bg_opacity
        )

        # Save the final image
        save_image(final_image, f"final_offer_image_{time.time()}.png")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
