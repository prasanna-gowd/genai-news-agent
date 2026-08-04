import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class ResearchService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        prompt_path = os.path.join(
            base_dir,
            "prompts",
            "research_prompt.txt"
        )

        with open(prompt_path, "r", encoding="utf-8") as file:
            self.prompt_template = file.read()

        self.model = "gemini-flash-latest"

    def analyze(self, article_text):

        prompt = self.prompt_template.replace(
            "{article}",
            article_text
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        try:
            data = json.loads(text)

        except Exception:

            data = {
                "headline": "",
                "summary": text,
                "short_summary": "",
                "key_points": [],
                "people": [],
                "organizations": [],
                "locations": [],
                "category": "Other",
                "importance_score": 5,
                "hashtags": [],
                "sentiment": "Neutral",
                "image_description": "",
                "seo_keywords": [],
                "fact_check_notes": "",
                "language": "English"
            }

        return data