from fastapi import APIRouter, HTTPException
from app.schemas.sem import SEMRequest, SEMResponse
from app.services.sem_service import run_sem

router = APIRouter()

# app/api/v1/endpoints/sem.py
@router.post("/analyze", response_model=SEMResponse)
def analyze_sem(req: SEMRequest):
    try:
        fit = run_sem(req.measurement, req.structural, req.data)
        return fit
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

