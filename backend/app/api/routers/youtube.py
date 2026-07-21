from fastapi import APIRouter, Body
from app.schemas.response import APIResponse
from app.modules.downloader.service import DownloaderService
from pydantic import BaseModel

router = APIRouter(tags=["YouTube"])

class YouTubeRequest(BaseModel):
    url: str

@router.post("/youtube", response_model=APIResponse)
async def upload_youtube_video(request: YouTubeRequest = Body(...)):
    """Downloads a YouTube video and starts processing."""
    metadata = await DownloaderService.process_youtube_upload(request.url)
    
    return APIResponse(
        success=True,
        message="Video downloaded successfully.",
        data={
            "job_id": metadata["job_id"],
            "status": "processing",
            "title": metadata["original_filename"]
        }
    )
