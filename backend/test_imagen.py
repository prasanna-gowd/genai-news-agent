import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt="A red apple on a wooden table",
    )

    print("Success!")
    print(response)

except Exception as e:
    print(type(e).__name__)
    print(e)