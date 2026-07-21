from fastapi import APIRouter, Depends
from app.api.auth import get_current_user
from app.api.routers import (
    health,
    upload,
    youtube,
    status,
    summary,
    notes,
    transcript,
    ocr,
    code,
    download
)

api_router = APIRouter(dependencies=[Depends(get_current_user)])

api_router.include_router(health.router)
api_router.include_router(upload.router)
api_router.include_router(youtube.router)
api_router.include_router(status.router)
api_router.include_router(summary.router)
api_router.include_router(notes.router)
api_router.include_router(transcript.router)
api_router.include_router(ocr.router)
api_router.include_router(code.router)
api_router.include_router(download.router)
