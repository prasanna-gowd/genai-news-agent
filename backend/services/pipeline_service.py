from datetime import datetime
import traceback

from services.news_service import NewsService
from services.scraper_service import ScraperService
from services.research_service import ResearchService
from services.ranking_service import RankingService
from services.caption_service import CaptionService
from services.image_prompt_service import ImagePromptService
from database.mongodb import MongoDB


class PipelineService:

    def __init__(self):

        self.news = NewsService()
        self.scraper = ScraperService()
        self.research = ResearchService()
        self.rank = RankingService()
        self.caption = CaptionService()
        self.image_prompt = ImagePromptService()
        self.db = MongoDB()

    def run(self, city="Anantapur"):

        stats = {
            "processed": 0,
            "saved": 0,
            "failed": 0,
            "duplicates": 0
        }

        print("\n========================================")
        print("      LocalPulse AI News Pipeline")
        print("========================================")
        print(f"City : {city}\n")

        articles = self.news.fetch_news(city)

        print(f"Fetched {len(articles)} articles.\n")

        for article in articles:

            stats["processed"] += 1

            print("=" * 60)
            print(f"Processing Article #{stats['processed']}")
            print(article.get("title"))
            print("=" * 60)

            try:

                article_hash = article.get("hash")

                # Duplicate Check
                if article_hash and self.db.is_duplicate(article_hash):
                    stats["duplicates"] += 1
                    print("Duplicate article. Skipping...\n")
                    continue

                # ----------------------------
                # Scrape Article
                # ----------------------------
                print("Scraping article...")

                article_data = self.scraper.extract_article(
                    article["url"]
                )

                if article_data is None:
                    raise Exception("Article scraping returned None.")

                full_text = article_data.get("text", "").strip()

                if not full_text:
                    raise Exception("Article text is empty.")

                print("Article scraped successfully.")

                # ----------------------------
                # AI Research
                # ----------------------------
                print("Generating research...")

                research = self.research.analyze(full_text)

                if not research:
                    raise Exception("Research generation failed.")

                print("Research generated.")

                # ----------------------------
                # Ranking
                # ----------------------------
                print("Calculating ranking...")

                score = self.rank.calculate(research)

                print(f"Importance Score : {score}")

                # ----------------------------
                # Caption
                # ----------------------------
                print("Generating caption...")

                caption = self.caption.generate(research)

                print("Caption generated.")

                # ----------------------------
                # Image Prompt
                # ----------------------------
                print("Generating image prompt...")

                image_prompt = self.image_prompt.generate(research)

                print("Image prompt generated.")

                # ----------------------------
                # Save
                # ----------------------------
                now = datetime.utcnow()

                document = {
                    "hash": article_hash,
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "published": article.get("published"),
                    "city": city,

                    "scraped_article": article_data,

                    "research": research,

                    "importance_score": score,

                    "caption": caption,

                    "image_prompt": image_prompt,

                    "status": "PENDING_APPROVAL",

                    "created_at": now,
                    "updated_at": now
                }

                self.db.save_article(document)
                self.db.save_research(article_hash, research)

                stats["saved"] += 1

                print("Article saved successfully.\n")

            except Exception:

                stats["failed"] += 1

                print("\nERROR OCCURRED")
                traceback.print_exc()
                print()

        print("\n========================================")
        print("Pipeline Finished")
        print("========================================")
        print(f"Processed  : {stats['processed']}")
        print(f"Saved      : {stats['saved']}")
        print(f"Duplicates : {stats['duplicates']}")
        print(f"Failed     : {stats['failed']}")
        print("========================================\n")

        return stats