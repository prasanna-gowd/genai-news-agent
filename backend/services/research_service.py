import json
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


class ResearchService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # backend/prompts/research_prompt.txt
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        prompt_path = os.path.join(
            base_dir,
            "prompts",
            "research_prompt.txt"
        )

        if not os.path.exists(prompt_path):
            raise FileNotFoundError(
                f"Research prompt not found: {prompt_path}"
            )

        with open(
            prompt_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.prompt_template = file.read()

        # Stable, low-cost model designed for
        # high-volume structured extraction.
        self.model = "gemini-3.5-flash-lite"

    # ============================================================
    # DEFAULT FALLBACK
    # ============================================================

    def fallback_result(self, article_text):

        text = (article_text or "").strip()

        short_summary = text[:300]

        return {
            "headline": "",
            "summary": text,
            "short_summary": short_summary,
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
            "fact_check_notes": (
                "AI research unavailable. "
                "Article retained for manual review."
            ),
            "language": "English",
            "research_status": "UNAVAILABLE"
        }

    # ============================================================
    # ANALYZE ARTICLE
    # ============================================================

    def analyze(self, article_text):

        article_text = (article_text or "").strip()

        if not article_text:
            return self.fallback_result("")

        prompt = self.prompt_template.replace(
            "{article}",
            article_text
        )

        # --------------------------------------------------------
        # Try Gemini
        # --------------------------------------------------------

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = (response.text or "").strip()

            if not text:
                print(
                    "WARNING: Gemini returned an empty response."
                )

                return self.fallback_result(
                    article_text
                )

            # ----------------------------------------------------
            # Remove markdown JSON fences
            # ----------------------------------------------------

            if text.startswith("```"):

                text = (
                    text
                    .replace("```json", "")
                    .replace("```JSON", "")
                    .replace("```", "")
                    .strip()
                )

            # ----------------------------------------------------
            # Parse JSON
            # ----------------------------------------------------

            try:

                data = json.loads(text)

            except json.JSONDecodeError:

                print(
                    "WARNING: Gemini returned invalid JSON."
                )

                return {
                    "headline": "",
                    "summary": text,
                    "short_summary": text[:300],
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
                    "language": "English",
                    "research_status": "COMPLETED"
                }

            # ----------------------------------------------------
            # Mark successful research
            # ----------------------------------------------------

            data.setdefault(
                "research_status",
                "COMPLETED"
            )

            return data

        # --------------------------------------------------------
        # Gemini quota / rate limit
        # --------------------------------------------------------

        except Exception as exc:

            error_text = str(exc)

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "quota" in error_text.lower()
                or "rate limit" in error_text.lower()
            ):

                print(
                    "WARNING: Gemini quota/rate limit reached."
                )

                print(
                    "Article will be retained without AI research."
                )

                return self.fallback_result(
                    article_text
                )

            # ----------------------------------------------------
            # Other Gemini error
            # ----------------------------------------------------

            print(
                "WARNING: Gemini research failed:"
            )

            print(error_text)

            return self.fallback_result(
                article_text
            )