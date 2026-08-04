class RankingService:

    def calculate(self, research):

        score = research.get("importance_score", 5)
        category = research.get("category", "").strip()

        if category == "Government":
            score += 2

        elif category == "Infrastructure":
            score += 2

        elif category == "Crime":
            score += 1

        elif category == "Education":
            score += 1

        return min(score, 10)