from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from services.pipeline_service import PipelineService
from database.mongodb import MongoDB


app = FastAPI(
    title="LocalPulse AI News Agent",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "https://genai-news-agent-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SERVICES
# ============================================================

pipeline = PipelineService()
db = MongoDB()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "message": "LocalPulse AI News Agent is Running"
    }


# ============================================================
# RUN PIPELINE
# ============================================================

@app.post("/pipeline/run")
def run_pipeline(city: str = "Anantapur"):
    try:
        result = pipeline.run(city)

        return {
            "success": True,
            "result": result
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Pipeline execution failed.",
                "detail": str(exc)
            }
        )


# ============================================================
# PENDING ARTICLES
# ============================================================

@app.get("/pending")
def pending_articles():
    try:
        articles = db.get_pending_articles()

        return {
            "count": len(articles),
            "articles": articles
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to load pending articles.",
                "detail": str(exc)
            }
        )


# ============================================================
# ALL ARTICLES
# ============================================================

@app.get("/articles")
def all_articles():
    try:
        articles = db.get_all_articles()

        return {
            "count": len(articles),
            "articles": articles
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to load articles.",
                "detail": str(exc)
            }
        )


# ============================================================
# SINGLE ARTICLE
# ============================================================

@app.get("/article/{article_hash}")
def article(article_hash: str):
    try:
        data = db.get_article(article_hash)

        if data is None:
            raise HTTPException(
                status_code=404,
                detail="Article not found."
            )

        return data

    except HTTPException:
        raise

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to load article.",
                "detail": str(exc)
            }
        )


# ============================================================
# APPROVE
# ============================================================

@app.post("/approve/{article_hash}")
def approve(article_hash: str):
    try:
        db.approve_article(article_hash)

        return {
            "message": "Article approved successfully."
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to approve article.",
                "detail": str(exc)
            }
        )


# ============================================================
# APPROVE ALL
# ============================================================

@app.post("/approve-all")
def approve_all():
    try:
        approved = db.approve_all_articles()

        return {
            "success": True,
            "approved": approved
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Failed to approve articles.",
                "detail": str(exc)
            }
        )


# ============================================================
# REJECT
# ============================================================

@app.post("/reject/{article_hash}")
def reject(article_hash: str):
    try:
        db.reject_article(article_hash)

        return {
            "message": "Article rejected successfully."
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to reject article.",
                "detail": str(exc)
            }
        )


# ============================================================
# DELETE
# ============================================================

@app.delete("/delete/{article_hash}")
def delete(article_hash: str):
    try:
        db.delete_article(article_hash)

        return {
            "message": "Article deleted successfully."
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to delete article.",
                "detail": str(exc)
            }
        )


# ============================================================
# STATUS
# ============================================================

@app.get("/status/{status}")
def articles_by_status(status: str):
    try:
        articles = db.get_articles_by_status(status.upper())

        return {
            "count": len(articles),
            "articles": articles
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to load articles by status.",
                "detail": str(exc)
            }
        )


# ============================================================
# STATS
# ============================================================

@app.get("/stats")
def stats():
    try:
        return db.get_stats()

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to load statistics.",
                "detail": str(exc)
            }
        )