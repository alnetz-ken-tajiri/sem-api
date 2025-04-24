# api/v1/endpoints/summarize.py
from fastapi import APIRouter, HTTPException
from app.schemas.summarize import SummarizeRequest, SummarizeResponse
from app.services.summarize_service import summarize

router = APIRouter()

@router.post("/", response_model=SummarizeResponse)
def summarize_article(req: SummarizeRequest):
    try:
        return {"summary": summarize(req.url)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
