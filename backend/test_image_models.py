import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Image Models:\n")

for model in client.models.list():

    name = model.name

    if "imagen" in name.lower():
        print(name)