from openai import OpenAI
from config import Config


class TextGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def generate_offer_text(self, prompt: str, word_limit: int) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant that generates short, catchy hotel offers."},
                    {"role": "user",
                     "content": f"Generate a short, catchy hotel offer based on the following prompt: {prompt}. The offer should be approximately {word_limit} words long."}
                ],
                max_tokens=100
            )
            return completion.choices[0].message.content.strip().replace('"', '')
        except Exception as e:
            print(f"Error in generating offer text: {str(e)}")
            return f"Special offer for {prompt}!"
