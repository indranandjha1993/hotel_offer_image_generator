import logging
from typing import Tuple

from PIL import Image

from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator
from models import TextStyle
from services.image_processor import ImageProcessor


class OfferGeneratorService:
    def __init__(self, text_generator: TextGenerator, image_generator: ImageGenerator, image_processor: ImageProcessor):
        self.text_generator = text_generator
        self.image_generator = image_generator
        self.image_processor = image_processor
        self.logger = logging.getLogger(__name__)

    def generate_offer(self, prompt: str, word_limit: int, style: TextStyle) -> Tuple[str, Image.Image, Image.Image]:
        try:
            offer_text = self.text_generator.generate_offer_text(prompt, word_limit)
            initial_image = self.image_generator.generate_image(prompt)
            final_image = self.image_processor.overlay_text_on_image(initial_image.copy(), offer_text, style)
            return offer_text, initial_image, final_image
        except Exception as e:
            self.logger.error(f"Error generating offer: {str(e)}")
            raise
