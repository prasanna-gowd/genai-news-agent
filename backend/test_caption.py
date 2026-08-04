from services.caption_service import CaptionService
from services.research_service import ResearchService

research = ResearchService()
caption = CaptionService()

article = """
The Andhra Pradesh Government inaugurated
a new waste processing plant in Anantapur.
"""

research_json = research.analyze(article)

print(caption.generate(research_json))