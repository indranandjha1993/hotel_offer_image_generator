import os
import time
from io import BytesIO

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
DEFAULT_FONT = "Arial.ttf"

# Ensure necessary folders exist
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(FONTS_FOLDER, exist_ok=True)

TEXT_POSITIONS = {
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

TEXT_COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0)
}

BACKGROUND_COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0)
}

FONT_SIZES = [12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72]


def generate_offer_text(prompt, word_limit):
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


def generate_image(prompt):
    """Generate an image using DALL-E model."""
    """Supported Image Resolutions ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024'] """
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
        image = Image.open(BytesIO(image_response.content))
        return image
    except Exception as e:
        print(f"Error in generating image: {str(e)}")
        return Image.new('RGB', (1024, 1024), color='white')


def get_font(font_name, size):
    """Get font object based on name and size."""
    font_path = os.path.join(FONTS_FOLDER, font_name)
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        print(f"Font {font_name} not found. Using default font.")
        return ImageFont.load_default().font_variant(size=size)


def overlay_text_on_image(image, text, font_name, font_size, position, text_color, bg_color, bg_opacity):
    """Overlay text on the image with customized options."""
    try:
        draw = ImageDraw.Draw(image, 'RGBA')
        font = get_font(font_name, font_size)

        image_width, image_height = image.size

        # Calculate text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Determine text position using text width and height
        if callable(TEXT_POSITIONS[position]):
            text_position = TEXT_POSITIONS[position](text_width, text_height, image_width, image_height)
        else:
            text_position = TEXT_POSITIONS[position]

        # Create a semi-transparent background with calculated opacity
        bg_color_with_opacity = bg_color + (int(bg_opacity * 255),)
        background_bbox = (
            text_position[0] - 5,
            text_position[1] - 5,
            text_position[0] + text_width + 5,
            text_position[1] + text_height + 5
        )
        draw.rectangle(background_bbox, fill=bg_color_with_opacity)

        # Draw text
        draw.text(text_position, text, font=font, fill=text_color)

        return image
    except Exception as e:
        print(f"Error in overlaying text: {str(e)}")
        return image


def save_image(image, filename):
    """Save image to the images folder."""
    filepath = os.path.join(IMAGES_FOLDER, filename)
    image.save(filepath)
    print(f"Image saved as: {filepath}")


def get_user_choice(prompt, options):
    """Get user choice from a list of options."""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    try:
        prompt = input("Enter the hotel offer prompt: ")
        word_limit = int(input("Enter word limit (default 5): ") or "5")

        # Generate and save the initial image
        initial_image = generate_image(prompt)
        save_image(initial_image, f"generated_image_{time.time()}.png")

        # Generate offer text
        offer_text = generate_offer_text(prompt, word_limit)
        print(f"Generated offer text: {offer_text}")

        # Get user preferences for text overlay
        font_name = get_user_choice("Choose a font:", os.listdir(FONTS_FOLDER)) or DEFAULT_FONT
        font_size = get_user_choice("Choose font size:", FONT_SIZES)
        text_position = get_user_choice("Choose text position:", list(TEXT_POSITIONS.keys()))
        text_color = get_user_choice("Choose text color:", list(TEXT_COLORS.keys()))
        bg_color = get_user_choice("Choose background color:", list(BACKGROUND_COLORS.keys()))
        bg_opacity = float(input("Enter background opacity (0.0 to 1.0, default 0.5): ") or "0.5")

        # Apply text overlay
        final_image = overlay_text_on_image(
            initial_image.copy(),
            offer_text,
            font_name,
            font_size,
            text_position,
            TEXT_COLORS[text_color],
            BACKGROUND_COLORS[bg_color],
            bg_opacity
        )

        # Save the final image
        save_image(final_image, f"final_offer_image_{time.time()}.png")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
