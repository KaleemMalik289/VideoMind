from fastapi import APIRouter
from app.schemas.response import APIResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=APIResponse)
async def health_check():
    """Checks if the API is running."""
    return APIResponse(success=True, message="VideoMind API is fully operational.")
