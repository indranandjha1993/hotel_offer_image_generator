from io import BytesIO
import requests
from PIL import Image
from openai import OpenAI
from config import Config


class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def generate_image(self, prompt: str) -> Image.Image:
        try:
            response = self.client.images.generate(
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
