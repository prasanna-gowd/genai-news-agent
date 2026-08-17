import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("=" * 80)
print("IMAGE MODELS")
print("=" * 80)

for model in client.models.list():

    name = model.name.lower()

    if (
        "image" in name
        or "imagen" in name
        or "vision" in name
    ):
        print(model.name)

print("\n")
print("=" * 80)
print("ALL GEMINI MODELS")
print("=" * 80)

for model in client.models.list():
    print(model.name)