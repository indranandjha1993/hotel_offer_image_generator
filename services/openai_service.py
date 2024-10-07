from PIL import Image
from io import BytesIO
import requests
from openai import OpenAI

from configs.config import Config
from contaracts.ai_contract import TextGenerationService, ImageGenerationService


class OpenAITextService(TextGenerationService):
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.prompts = Config.load_prompts()['ai_prompts']['text_generation']

    def generate_text(self, prompt: str, word_limit: int) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.prompts['system_message']},
                    {"role": "user",
                     "content": self.prompts['user_message'].format(prompt=prompt, word_limit=word_limit)}
                ],
                max_tokens=100
            )
            return completion.choices[0].message.content.strip().replace('"', '')
        except Exception as e:
            print(f"Error in generating offer text: {str(e)}")
            return f"Special offer for {prompt}!"


class OpenAIImageService(ImageGenerationService):
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.prompts = Config.load_prompts()['ai_prompts']['image_generation']

    def generate_image(self, prompt: str) -> Image.Image:
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=self.prompts['prompt'].format(prompt=prompt),
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
