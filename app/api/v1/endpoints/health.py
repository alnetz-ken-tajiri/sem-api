# backend/app/api/v1/endpoints/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz", tags=["Health"])
def healthz():
    return {"status": "ok"}
