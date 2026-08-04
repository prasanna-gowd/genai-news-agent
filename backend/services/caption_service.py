import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class CaptionService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = "gemini-flash-latest"

        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        prompt_path = os.path.join(
            base_dir,
            "prompts",
            "caption_prompt.txt"
        )

        with open(
            prompt_path,
            "r",
            encoding="utf-8"
        ) as file:
            self.prompt_template = file.read()

    def generate(self, research):

        prompt = self.prompt_template.replace(
            "{news}",
            str(research)
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text.strip()