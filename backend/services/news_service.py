import os
import requests

from dotenv import load_dotenv
from services.hash_service import HashService

load_dotenv()

hash_service = HashService()


class NewsService:

    def __init__(self):
        self.api_key = os.getenv("GNEWS_API_KEY")

        if not self.api_key:
            raise ValueError("GNEWS_API_KEY not found in .env file")

    def fetch_news(self, city: str):

        url = (
            "https://gnews.io/api/v4/search"
            f"?q={city}"
            "&lang=en"
            "&country=in"
            "&max=20"
            f"&apikey={self.api_key}"
        )

        print(f"\nFetching news for: {city}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        articles = []

        for item in data.get("articles", []):

            article_url = item.get("url", "")
            title = item.get("title", "")

            article_hash = hash_service.generate(title + article_url)

            articles.append({
                "id": article_hash,
                "hash": article_hash,
                "title": title,
                "url": article_url,
                "link": article_url,
                "published": item.get("publishedAt", ""),
                "summary": item.get("description", ""),
                "source": item.get("source", {}).get("name", "")
            })

        print(f"Fetched {len(articles)} articles.\n")

        return articles