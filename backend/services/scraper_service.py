from newspaper import Article


class ScraperService:

    def extract_article(self, url):

        print("\n----------------------------------------")
        print("Scraping URL:")
        print(url)
        print("----------------------------------------")

        try:
            article = Article(url)

            article.download()
            article.parse()

            print(f"Title: {article.title}")
            print(f"Text Length: {len(article.text)}")

            if len(article.text.strip()) == 0:
                print("Warning: No article text extracted.")

            return {
                "title": article.title,
                "text": article.text,
                "authors": article.authors,
                "publish_date": str(article.publish_date)
            }

        except Exception as e:
            print(f"Scraper Error: {e}")
            return None