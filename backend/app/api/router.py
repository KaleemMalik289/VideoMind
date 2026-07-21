from fastapi import APIRouter
from app.modules.upload import router as upload_router

api_router = APIRouter()

# Register the upload routes under /api/v1/upload
api_router.include_router(upload_router.router, prefix="/upload", tags=["upload"])
