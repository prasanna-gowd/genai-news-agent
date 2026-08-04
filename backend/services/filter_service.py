BAD_KEYWORDS = [
    "gold",
    "silver",
    "price",
    "rate",
    "bike",
    "car",
    "mercedes",
    "aqi",
    "weather today"
]


class FilterService:

    def filter_articles(self, articles):

        filtered = []

        for article in articles:

            title = article["title"].lower()

            skip = False

            for keyword in BAD_KEYWORDS:

                if keyword in title:
                    skip = True
                    break

            if not skip:
                filtered.append(article)

        return filtered