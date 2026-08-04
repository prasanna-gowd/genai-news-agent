import hashlib


class HashService:

    def generate(self, text: str):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()