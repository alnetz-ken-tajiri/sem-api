# backend/app/api/v1/endpoints/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Health"])  # 👈 ここを "/" に変更
def healthz():
    return {"status": "ok"}