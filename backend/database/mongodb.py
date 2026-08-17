import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoDB:

    def __init__(self):

        self.client = MongoClient(
            os.getenv("MONGODB_URI")
        )

        self.db = self.client[
            os.getenv("DATABASE_NAME")
        ]

        self.articles = self.db["articles"]
        self.research = self.db["research_results"]

    # =====================================
    # SERIALIZATION
    # =====================================

    def serialize(self, document):

        if document is None:
            return None

        document["_id"] = str(document["_id"])

        return document

    def serialize_many(self, documents):

        return [self.serialize(doc) for doc in documents]

    # =====================================
    # DUPLICATE CHECK
    # =====================================

    def is_duplicate(self, article_hash):

        return self.articles.find_one(
            {"hash": article_hash}
        ) is not None

    # Compatibility
    def article_exists(self, article_hash):

        return self.is_duplicate(article_hash)

    # =====================================
    # SAVE ARTICLE
    # =====================================

    def save_article(self, article):

        self.articles.insert_one(article)

    # =====================================
    # SAVE RESEARCH
    # =====================================

    def save_research(self, article_hash, research):

        research["article_hash"] = article_hash

        self.research.replace_one(
            {"article_hash": article_hash},
            research,
            upsert=True
        )

    # =====================================
    # GET ALL ARTICLES
    # =====================================

    def get_all_articles(self):

        articles = list(
            self.articles.find({})
        )

        return self.serialize_many(articles)

    # =====================================
    # GET PENDING ARTICLES
    # =====================================

    def get_pending_articles(self):

        articles = list(
            self.articles.find(
                {"status": "PENDING_APPROVAL"}
            )
        )

        return self.serialize_many(articles)

    # =====================================
    # GET SINGLE ARTICLE
    # =====================================

    def get_article(self, article_hash):

        article = self.articles.find_one(
            {"hash": article_hash}
        )

        return self.serialize(article)

    # =====================================
    # UPDATE STATUS
    # =====================================

    def update_status(self, article_hash, status):

        self.articles.update_one(
            {"hash": article_hash},
            {
                "$set": {
                    "status": status
                }
            }
        )

    # =====================================
    # APPROVE
    # =====================================

    def approve_article(self, article_hash):

        self.update_status(
            article_hash,
            "APPROVED"
        )


    # =====================================
    # APPROVE ALL PENDING
    # =====================================

    def approve_all_articles(self):

        result = self.articles.update_many(
            {"status": "PENDING_APPROVAL"},
            {
                "$set": {
                    "status": "APPROVED"
                }
            }
        )

        return result.modified_count

    # =====================================
    # REJECT
    # =====================================

    def reject_article(self, article_hash):

        self.update_status(
            article_hash,
            "REJECTED"
        )

    # =====================================
    # DELETE
    # =====================================

    def delete_article(self, article_hash):

        self.articles.delete_one(
            {"hash": article_hash}
        )

        self.research.delete_one(
            {"article_hash": article_hash}
        )

    # =====================================
    # GET BY STATUS
    # =====================================

    def get_articles_by_status(self, status):

        articles = list(
            self.articles.find(
                {"status": status}
            )
        )

        return self.serialize_many(articles)

    # =====================================
    # DATABASE STATS
    # =====================================

    def get_stats(self):

        # Articles grouped by category
        cat_pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        by_category = {
            (d["_id"] or "unknown"): d["count"]
            for d in self.articles.aggregate(cat_pipeline)
        }

        # Articles grouped by published date (last 14 days)
        # Handles both datetime objects and ISO string fields
        day_pipeline = [
            {
                "$addFields": {
                    "pub_date": {
                        "$cond": {
                            "if": {"$eq": [{"$type": "$published"}, "date"]},
                            "then": {
                                "$dateToString": {
                                    "format": "%Y-%m-%d",
                                    "date": "$published"
                                }
                            },
                            "else": {
                                "$substr": [{"$ifNull": ["$published", ""]}, 0, 10]
                            }
                        }
                    }
                }
            },
            {"$match": {"pub_date": {"$ne": ""}}},
            {"$group": {"_id": "$pub_date", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
            {"$limit": 14}
        ]
        by_day = [
            {"date": d["_id"], "count": d["count"]}
            for d in self.articles.aggregate(day_pipeline)
            if d["_id"]
        ]

        return {
            "total_articles": self.articles.count_documents({}),
            "pending": self.articles.count_documents(
                {"status": "PENDING_APPROVAL"}
            ),
            "approved": self.articles.count_documents(
                {"status": "APPROVED"}
            ),
            "rejected": self.articles.count_documents(
                {"status": "REJECTED"}
            ),
            "research_documents": self.research.count_documents({}),
            "articles_by_category": by_category,
            "articles_by_day": by_day
        }