import logging
from typing import Tuple, Callable
from PIL import Image
from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator
from models import TextStyle
from services.image_processor import ImageProcessor


class OfferGeneratorService:
    def __init__(
        self,
        text_generator: TextGenerator,
        image_generator: ImageGenerator,
        image_processor: ImageProcessor,
    ):
        self.text_generator = text_generator
        self.image_generator = image_generator
        self.image_processor = image_processor
        self.logger = logging.getLogger(__name__)

    def generate_offer(
        self,
        prompt: str,
        word_limit: int,
        style: TextStyle,
        text_progress: Callable[[float], None] = None,
        image_progress: Callable[[float], None] = None,
        overlay_progress: Callable[[float], None] = None,
    ) -> Tuple[str, Image.Image, Image.Image]:
        try:
            offer_text = self.text_generator.generate_offer_text(
                prompt, word_limit, progress_callback=text_progress
            )
            initial_image = self.image_generator.generate_image(
                prompt, progress_callback=image_progress
            )
            final_image = self.image_processor.overlay_text_on_image(
                initial_image.copy(),
                offer_text,
                style,
                progress_callback=overlay_progress,
            )
            return offer_text, initial_image, final_image
        except Exception as e:
            self.logger.error(f"Error generating offer: {str(e)}")
            raise
