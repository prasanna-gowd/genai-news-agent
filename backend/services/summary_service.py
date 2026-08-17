import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class SummaryService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = "gemini-2.5-flash"

        prompt_path = os.path.join(
            "prompts",
            "summary_prompt.txt"
        )

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def summarize(self, article):

        article_text = article.get(
            "scraped_article",
            {}
        ).get(
            "text",
            ""
        )

        title = article.get("title", "")

        prompt = f"""
{self.system_prompt}

TITLE:
{title}

ARTICLE:
{article_text}
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            output = response.text.strip()

            # Remove markdown if Gemini returns ```json
            output = output.replace("```json", "")
            output = output.replace("```", "")
            output = output.strip()

            return json.loads(output)

        except Exception as e:

            print("Summary Error:", e)

            return {
                "headline": title,
                "summary": "Summary generation failed."
            }