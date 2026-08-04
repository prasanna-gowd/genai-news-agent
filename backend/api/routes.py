from fastapi import APIRouter

from services.pipeline_service import PipelineService

router = APIRouter()

pipeline = PipelineService()


@router.get("/")
def home():

    return {
        "message": "AI News Agent API is running."
    }


@router.post("/pipeline/run")
def run_pipeline(city: str = "Anantapur"):

    result = pipeline.run(city)

    return {
        "success": True,
        "result": result
    }