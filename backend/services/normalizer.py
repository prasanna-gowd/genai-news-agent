from models.article import Article


class Normalizer:

    def normalize(self, raw_articles, city):

        articles = []

        for item in raw_articles:

            article = Article(
                id=item["id"],
                hash=item["id"],
                title=item["title"],
                url=item["link"],
                source=item["source"],
                published_at=item["published"],
                city=city
            )

            articles.append(article.model_dump())

        return articles