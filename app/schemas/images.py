# schemas/images.py
from pydantic import BaseModel

class ImageFetchRequest(BaseModel):
    url: str

class ImageFetchResponse(BaseModel):
    images: list[str]
