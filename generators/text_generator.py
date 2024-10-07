from typing import Callable
from factories.ai_service_factory import AIServiceFactory


class TextGenerator:
    def __init__(self, service_name: str = "openai"):
        self.service = AIServiceFactory.get_text_service(service_name)

    def generate_offer_text(self, prompt: str, word_limit: int,
                            progress_callback: Callable[[float], None] = None) -> str:
        text = self.service.generate_text(prompt, word_limit)
        if progress_callback:
            progress_callback(100)  # Assuming text generation is a single step process
        return text
   