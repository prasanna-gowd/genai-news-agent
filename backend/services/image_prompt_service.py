import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class ImagePromptService:

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
            "image_prompt.txt"
        )

        with open(
            prompt_path,
            "r",
            encoding="utf-8"
        ) as file:
            self.prompt_template = file.read()

    def generate(self, research):

        prompt = self.prompt_template

        prompt = prompt.replace(
            "{headline}",
            research.get("headline", "")
        )

        prompt = prompt.replace(
            "{summary}",
            research.get("summary", "")
        )

        prompt = prompt.replace(
            "{image_description}",
            research.get("image_description", "")
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text.strip()