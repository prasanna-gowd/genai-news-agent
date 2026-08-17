from services.research_service import ResearchService
from services.image_prompt_service import ImagePromptService
from services.image_generation_service import ImageGenerationService


article = """
The Andhra Pradesh Government inaugurated
a new waste processing plant in Anantapur.
The project aims to improve waste management,
create employment, and promote sustainable development.
"""

print("=" * 70)
print("Generating Research...")
print("=" * 70)

research = ResearchService()
research_json = research.analyze(article)

print("✅ Research Generated\n")

print("=" * 70)
print("Generating Image Prompt...")
print("=" * 70)

prompt_service = ImagePromptService()
image_prompt = prompt_service.generate(research_json)

print(image_prompt)

print("\n✅ Image Prompt Generated\n")

print("=" * 70)
print("Generating Image...")
print("=" * 70)

generator = ImageGenerationService()

image_path = generator.generate(image_prompt)

print("\n✅ Image Saved Successfully")
print(image_path)