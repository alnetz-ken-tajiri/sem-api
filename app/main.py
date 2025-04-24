
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import sem  # ← 追記
from app.api.v1.endpoints import health, summarize, images

app = FastAPI(title="Scraping & SEM API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sem.router, prefix="/api/v1/sem",
                   tags=["SEM"])
app.include_router(summarize.router, prefix="/api/v1/summarize",
                   tags=["Summarize"])
app.include_router(images.router, prefix="/api/v1/images",
                   tags=["Images"])
app.include_router(health.router, prefix="/api/v1/health",
                   tags=["Health"])
