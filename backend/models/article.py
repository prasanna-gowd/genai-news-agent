from pydantic import BaseModel


class Article(BaseModel):
    id: str
    title: str
    description: str = ""
    content: str = ""
    url: str
    source: str
    published_at: str
    city: str
    language: str = "en"
    category: str = "unknown"
    hash: str