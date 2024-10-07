from PIL import Image

from factories.ai_service_factory import AIServiceFactory


class ImageGenerator:
    def __init__(self, service_name: str = "openai"):
        self.service = AIServiceFactory.get_image_service(service_name)

    def generate_image(self, prompt: str) -> Image.Image:
        return self.service.generate_image(prompt)
