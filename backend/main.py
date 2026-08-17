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
        # Local development
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",

        # Production frontend
        "https://genai-news-agent-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# Services
# ==========================

pipeline = PipelineService()
db = MongoDB()


# ==========================
# HOME / HEALTH CHECK
# ==========================

@app.get("/")
def home():
    return {
        "message": "LocalPulse AI News Agent is Running 🚀"
    }


# ==========================
# RUN AI PIPELINE
# ==========================

@app.post("/pipeline/run")
def run_pipeline(city: str = "Anantapur"):

    result = pipeline.run(city)

    return {
        "success": True,
        "result": result
    }


# ==========================
# PENDING ARTICLES
# ==========================

@app.get("/pending")
def pending_articles():

    articles = db.get_pending_articles()

    return {
        "count": len(articles),
        "articles": articles
    }


# ==========================
# ALL ARTICLES
# ==========================

@app.get("/articles")
def all_articles():

    articles = db.get_all_articles()

    return {
        "count": len(articles),
        "articles": articles
    }


# ==========================
# SINGLE ARTICLE
# ==========================

@app.get("/article/{article_hash}")
def article(article_hash: str):

    data = db.get_article(article_hash)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found."
        )

    return data


# ==========================
# APPROVE ARTICLE
# ==========================

@app.post("/approve/{article_hash}")
def approve(article_hash: str):

    db.approve_article(article_hash)

    return {
        "message": "Article approved successfully."
    }


# ==========================
# APPROVE ALL ARTICLES
# ==========================

@app.post("/approve-all")
def approve_all():

    approved = db.approve_all_articles()

    return {
        "success": True,
        "approved": approved
    }


# ==========================
# REJECT ARTICLE
# ==========================

@app.post("/reject/{article_hash}")
def reject(article_hash: str):

    db.reject_article(article_hash)

    return {
        "message": "Article rejected successfully."
    }


# ==========================
# DELETE ARTICLE
# ==========================

@app.delete("/delete/{article_hash}")
def delete(article_hash: str):

    db.delete_article(article_hash)

    return {
        "message": "Article deleted successfully."
    }


# ==========================
# ARTICLES BY STATUS
# ==========================

@app.get("/status/{status}")
def articles_by_status(status: str):

    articles = db.get_articles_by_status(
        status.upper()
    )

    return {
        "count": len(articles),
        "articles": articles
    }


# ==========================
# DATABASE STATISTICS
# ==========================

@app.get("/stats")
def stats():

    return db.get_stats()