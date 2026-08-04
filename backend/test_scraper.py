from services.scraper_service import ScraperService

scraper = ScraperService()

url = "https://www.thehindu.com/news/national/andhra-pradesh/"

result = scraper.extract_article(url)

print(result)