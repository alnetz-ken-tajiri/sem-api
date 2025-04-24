# api/v1/endpoints/images.py
from fastapi import APIRouter, HTTPException
from app.schemas.images import ImageFetchRequest, ImageFetchResponse
from app.services.image_service import extract_images

router = APIRouter()

@router.post("/", response_model=ImageFetchResponse)
def fetch_images(req: ImageFetchRequest):
    try:
        return {"images": extract_images(req.url)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
