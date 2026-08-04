from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.pipeline_service import PipelineService
from database.mongodb import MongoDB

app = FastAPI(
    title="LocalPulse AI News Agent",
    version="1.0.0"
)

# ==========================
# CORS Configuration
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = PipelineService()
db = MongoDB()


@app.get("/")
def home():
    return {
        "message": "LocalPulse AI News Agent is Running 🚀"
    }


# ---------------------------
# Run AI Pipeline
# ---------------------------
@app.post("/pipeline/run")
def run_pipeline(city: str = "Anantapur"):

    result = pipeline.run(city)

    return {
        "success": True,
        "result": result
    }


# ---------------------------
# Pending Articles
# ---------------------------
@app.get("/pending")
def pending_articles():

    articles = db.get_pending_articles()

    return {
        "count": len(articles),
        "articles": articles
    }


# ---------------------------
# All Articles
# ---------------------------
@app.get("/articles")
def all_articles():

    articles = db.get_all_articles()

    return {
        "count": len(articles),
        "articles": articles
    }


# ---------------------------
# Single Article
# ---------------------------
@app.get("/article/{article_hash}")
def article(article_hash: str):

    data = db.get_article(article_hash)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found."
        )

    return data


# ---------------------------
# Approve
# ---------------------------
@app.post("/approve/{article_hash}")
def approve(article_hash: str):

    db.approve_article(article_hash)

    return {
        "message": "Article approved successfully."
    }


# ---------------------------
# Reject
# ---------------------------
@app.post("/reject/{article_hash}")
def reject(article_hash: str):

    db.reject_article(article_hash)

    return {
        "message": "Article rejected successfully."
    }


# ---------------------------
# Delete
# ---------------------------
@app.delete("/delete/{article_hash}")
def delete(article_hash: str):

    db.delete_article(article_hash)

    return {
        "message": "Article deleted successfully."
    }


# ---------------------------
# Status
# ---------------------------
@app.get("/status/{status}")
def articles_by_status(status: str):

    articles = db.get_articles_by_status(
        status.upper()
    )

    return {
        "count": len(articles),
        "articles": articles
    }


# ---------------------------
# Stats
# ---------------------------
@app.get("/stats")
def stats():

    return db.get_stats()