import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class ImageGenerationService:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = "gemini-3.1-flash-image"

    def generate(self, prompt, filename="news_image"):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        os.makedirs("images", exist_ok=True)

        for candidate in response.candidates:
            for part in candidate.content.parts:

                if hasattr(part, "inline_data") and part.inline_data:

                    image_bytes = part.inline_data.data

                    path = os.path.join(
                        "images",
                        f"{filename}.png"
                    )

                    with open(path, "wb") as f:
                        f.write(image_bytes)

                    return path

        raise Exception("No image was returned.")