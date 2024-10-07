from abc import ABC, abstractmethod
from PIL import Image


class TextGenerationService(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, word_limit: int) -> str:
        pass


class ImageGenerationService(ABC):
    @abstractmethod
    def generate_image(self, prompt: str) -> Image.Image:
        pass
