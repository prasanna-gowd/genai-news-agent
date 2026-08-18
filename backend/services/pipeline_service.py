from datetime import datetime
import traceback

from services.image_generation_service import ImageGenerationService
from services.news_service import NewsService
from services.scraper_service import ScraperService
from services.research_service import ResearchService
from services.ranking_service import RankingService
from services.caption_service import CaptionService
from services.image_prompt_service import ImagePromptService
from services.summary_service import SummaryService

from database.mongodb import MongoDB


class PipelineService:

    def __init__(self):

        self.news = NewsService()
        self.scraper = ScraperService()

        # AI services
        self.research = ResearchService()
        self.summary = SummaryService()
        self.rank = RankingService()
        self.caption = CaptionService()
        self.image_prompt = ImagePromptService()
        self.image_generator = ImageGenerationService()

        # Database
        self.db = MongoDB()

    # ============================================================
    # FALLBACK RESEARCH
    # ============================================================

    def _fallback_research(self, article):

        title = article.get("title", "")
        text = article.get("text", "")

        return {
            "headline": title,
            "summary": text[:1000],
            "short_summary": text[:300],
            "key_points": [],
            "people": [],
            "organizations": [],
            "locations": [],
            "category": "Other",
            "importance_score": 5,
            "hashtags": [],
            "sentiment": "Neutral",
            "image_description": "",
            "seo_keywords": [],
            "fact_check_notes": (
                "AI research unavailable. "
                "Article retained for manual review."
            ),
            "language": "English",
            "research_status": "UNAVAILABLE"
        }

    # ============================================================
    # RUN PIPELINE
    # ============================================================

    def run(self, city="Anantapur"):

        stats = {
            "processed": 0,
            "saved": 0,
            "failed": 0,
            "duplicates": 0,
            "research_failed": 0,
            "summary_failed": 0,
            "caption_failed": 0,
            "image_prompt_failed": 0,
            "image_failed": 0
        }

        print("\n========================================")
        print("      LocalPulse AI News Pipeline")
        print("========================================")
        print(f"City : {city}\n")

        # ========================================================
        # FETCH NEWS
        # ========================================================

        try:

            articles = self.news.fetch_news(city)

        except Exception as exc:

            print("\nNEWS FETCH FAILED")
            print(str(exc))
            traceback.print_exc()

            return stats

        print(f"Fetched {len(articles)} articles.\n")

        # ========================================================
        # PROCESS ARTICLES
        # ========================================================

        for article in articles:

            stats["processed"] += 1

            print("=" * 60)
            print(
                f"Processing Article #{stats['processed']}"
            )
            print(article.get("title"))
            print("=" * 60)

            try:

                article_hash = article.get("hash")

                # =================================================
                # DUPLICATE CHECK
                # =================================================

                if article_hash and self.db.is_duplicate(
                    article_hash
                ):

                    stats["duplicates"] += 1

                    print(
                        "Duplicate article. Skipping...\n"
                    )

                    continue

                # =================================================
                # SCRAPE ARTICLE
                # =================================================

                print("Scraping article...")

                try:

                    article_data = (
                        self.scraper.extract_article(
                            article["url"]
                        )
                    )

                except Exception as exc:

                    print(
                        "Scraping failed:"
                    )

                    print(str(exc))

                    article_data = None

                # -------------------------------------------------
                # If scraping fails, use RSS/article information
                # instead of throwing the article away.
                # -------------------------------------------------

                if not article_data:

                    print(
                        "Using news source data "
                        "because scraping failed."
                    )

                    article_data = {
                        "title": article.get(
                            "title",
                            ""
                        ),
                        "text": article.get(
                            "description",
                            ""
                        ),
                        "url": article.get(
                            "url",
                            ""
                        )
                    }

                full_text = (
                    article_data.get(
                        "text",
                        ""
                    )
                    or ""
                ).strip()

                # -------------------------------------------------
                # Make sure we at least have something to process.
                # -------------------------------------------------

                if not full_text:

                    full_text = (
                        article.get(
                            "title",
                            ""
                        )
                        or ""
                    )

                print(
                    "Article data available."
                )

                # =================================================
                # AI RESEARCH
                # =================================================

                print(
                    "Generating research..."
                )

                try:

                    research = self.research.analyze(
                        full_text
                    )

                    if not research:

                        raise Exception(
                            "Empty research response."
                        )

                    print(
                        "Research generated."
                    )

                except Exception as exc:

                    stats["research_failed"] += 1

                    print(
                        "Research failed."
                    )

                    print(str(exc))

                    research = self._fallback_research(
                        {
                            "title": article.get(
                                "title",
                                ""
                            ),
                            "text": full_text
                        }
                    )

                # =================================================
                # AI SUMMARY
                # =================================================

                print(
                    "Generating summary..."
                )

                try:

                    summary = self.summary.summarize(
                        {
                            "title": article.get(
                                "title"
                            ),
                            "scraped_article": article_data
                        }
                    )

                    if not summary:

                        raise Exception(
                            "Empty summary response."
                        )

                    print(
                        "Summary generated."
                    )

                except Exception as exc:

                    stats["summary_failed"] += 1

                    print(
                        "Summary failed:"
                    )

                    print(str(exc))

                    # ---------------------------------------------
                    # Fallback summary
                    # ---------------------------------------------

                    summary = {
                        "headline": article.get(
                            "title",
                            ""
                        ),
                        "summary": full_text[:1000],
                        "short_summary": full_text[:300]
                    }

                # =================================================
                # RANKING
                # =================================================

                print(
                    "Calculating ranking..."
                )

                try:

                    score = self.rank.calculate(
                        research
                    )

                except Exception as exc:

                    print(
                        "Ranking failed:"
                    )

                    print(str(exc))

                    score = research.get(
                        "importance_score",
                        5
                    )

                print(
                    f"Importance Score : {score}"
                )

                # =================================================
                # CAPTION
                # =================================================

                print(
                    "Generating caption..."
                )

                try:

                    caption = self.caption.generate(
                        research
                    )

                    if not caption:
                        caption = ""

                    print(
                        "Caption generated."
                    )

                except Exception as exc:

                    stats["caption_failed"] += 1

                    print(
                        "Caption generation failed:"
                    )

                    print(str(exc))

                    caption = ""

                # =================================================
                # IMAGE PROMPT
                # =================================================

                print(
                    "Generating image prompt..."
                )

                try:

                    image_prompt = (
                        self.image_prompt.generate(
                            research
                        )
                    )

                    if not image_prompt:
                        image_prompt = ""

                    print(
                        "Image prompt generated."
                    )

                except Exception as exc:

                    stats[
                        "image_prompt_failed"
                    ] += 1

                    print(
                        "Image prompt generation failed:"
                    )

                    print(str(exc))

                    image_prompt = ""

                # =================================================
                # AI IMAGE GENERATION
                # =================================================

                generated_image = None

                if image_prompt:

                    print(
                        "Generating AI image..."
                    )

                    try:

                        generated_image = (
                            self.image_generator.generate(
                                image_prompt
                            )
                        )

                        print(
                            f"Image saved: "
                            f"{generated_image}"
                        )

                    except Exception as exc:

                        stats["image_failed"] += 1

                        print(
                            "Image generation failed:"
                        )

                        print(str(exc))

                else:

                    print(
                        "Skipping image generation "
                        "because no image prompt exists."
                    )

                # =================================================
                # SAVE ARTICLE
                # =================================================

                print(
                    "Saving article to MongoDB..."
                )

                now = datetime.utcnow()

                # -------------------------------------------------
                # CATEGORY
                # -------------------------------------------------
                # Research normally contains a category.
                # If AI research fails, fallback research provides
                # "Other".
                # -------------------------------------------------

                category = research.get(
                    "category",
                    "Other"
                )

                if not category:
                    category = "Other"

                document = {

                    "hash": article_hash,

                    "title": article.get(
                        "title"
                    ),

                    "url": article.get(
                        "url"
                    ),

                    "published": article.get(
                        "published"
                    ),

                    "city": city,

                    "scraped_article":
                        article_data,

                    "research":
                        research,

                    "headline":
                        summary.get(
                            "headline",
                            article.get(
                                "title",
                                ""
                            )
                        ),

                    "summary":
                        summary.get(
                            "summary",
                            research.get(
                                "summary",
                                ""
                            )
                        ),

                    "short_summary":
                        summary.get(
                            "short_summary",
                            research.get(
                                "short_summary",
                                ""
                            )
                        ),

                    # NEW: Save category at top level
                    "category":
                        category,

                    "importance_score":
                        score,

                    "caption":
                        caption,

                    "image_prompt":
                        image_prompt,

                    "generated_image":
                        generated_image,

                    "status":
                        "PENDING_APPROVAL",

                    "created_at":
                        now,

                    "updated_at":
                        now
                }

                # =================================================
                # SAVE TO DATABASE
                # =================================================

                self.db.save_article(
                    document
                )

                self.db.save_research(
                    article_hash,
                    research
                )

                stats["saved"] += 1

                print(
                    "Article saved successfully."
                )

                print()

            # =====================================================
            # ARTICLE-LEVEL FAILURE
            # =====================================================

            except Exception as exc:

                stats["failed"] += 1

                print(
                    "\nARTICLE PROCESSING FAILED"
                )

                print(
                    str(exc)
                )

                traceback.print_exc()

                print()

        # ========================================================
        # PIPELINE SUMMARY
        # ========================================================

        print("\n========================================")
        print("Pipeline Finished")
        print("========================================")

        print(
            f"Processed          : "
            f"{stats['processed']}"
        )

        print(
            f"Saved              : "
            f"{stats['saved']}"
        )

        print(
            f"Duplicates         : "
            f"{stats['duplicates']}"
        )

        print(
            f"Failed             : "
            f"{stats['failed']}"
        )

        print(
            f"Research Failed    : "
            f"{stats['research_failed']}"
        )

        print(
            f"Summary Failed     : "
            f"{stats['summary_failed']}"
        )

        print(
            f"Caption Failed     : "
            f"{stats['caption_failed']}"
        )

        print(
            f"Image Prompt Failed: "
            f"{stats['image_prompt_failed']}"
        )

        print(
            f"Image Failed       : "
            f"{stats['image_failed']}"
        )

        print(
            "========================================\n"
        )

        return stats