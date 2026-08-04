from services.image_prompt_service import ImagePromptService
from services.research_service import ResearchService

research = ResearchService()
image = ImagePromptService()

article = """
The Andhra Pradesh Government inaugurated
a new waste processing plant in Anantapur.
"""

research_json = research.analyze(article)

print(image.generate(research_json))