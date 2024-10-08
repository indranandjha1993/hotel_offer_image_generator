from typing import Callable
from PIL import Image
from factories.ai_service_factory import AIServiceFactory


class ImageGenerator:
    def __init__(self, service_name: str = "openai"):
        self.service = AIServiceFactory.get_image_service(service_name)

    def generate_image(
        self, prompt: str, progress_callback: Callable[[float], None] = None
    ) -> Image.Image:
        image = self.service.generate_image(prompt)
        if progress_callback:
            progress_callback(100)  # Assuming image generation is a single step process
        return image
