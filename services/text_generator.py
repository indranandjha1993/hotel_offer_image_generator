from openai import OpenAI
from config import Config


class TextGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.prompts = Config.load_prompts()['ai_prompts']['text_generation']

    def generate_offer_text(self, prompt: str, word_limit: int) -> str:
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
