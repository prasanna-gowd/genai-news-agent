from services.research_service import ResearchService
import json

research = ResearchService()

article = """
The Andhra Pradesh Government inaugurated a new waste processing
plant in Anantapur to improve solid waste management.

The project is expected to reduce landfill waste and improve
environmental sustainability.

Officials said the facility will process hundreds of tons of
municipal waste every day.
"""

result = research.analyze(article)

print(json.dumps(result, indent=4))