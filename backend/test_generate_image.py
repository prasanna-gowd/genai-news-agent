from services.image_prompt_service import ImagePromptService
from services.image_generation_service import ImageGenerationService
from services.research_service import ResearchService

research = ResearchService()
prompt_service = ImagePromptService()
image_service = ImageGenerationService()

article = """
The Andhra Pradesh Government inaugurated
a new waste processing plant in Anantapur.
"""

research_json = research.analyze(article)

prompt = prompt_service.generate(research_json)

print("Prompt:")
print(prompt)

image = image_service.generate(
    prompt,
    filename="anantapur_news"
)

print("\nSaved Image:")
print(image)