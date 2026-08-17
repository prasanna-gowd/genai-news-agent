import os
import uuid

from dotenv import load_dotenv
from google import genai

load_dotenv()


class ImageGenerationService:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = "gemini-3.1-flash-image"

        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(self.output_dir, filename)

        for candidate in response.candidates:
            if not candidate.content:
                continue

            for part in candidate.content.parts:

                if getattr(part, "inline_data", None):

                    with open(filepath, "wb") as f:
                        f.write(part.inline_data.data)

                    return filepath

        raise RuntimeError(
            "Gemini did not return an image."
        )