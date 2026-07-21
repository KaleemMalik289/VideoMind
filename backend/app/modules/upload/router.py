from fastapi import APIRouter, UploadFile, File, Body
from app.modules.upload.schemas import LocalUploadResponse, YouTubeUploadRequest, YouTubeUploadResponse
from app.modules.upload.service import UploadService
from app.modules.downloader.service import DownloaderService

router = APIRouter()

@router.post("/video", response_model=LocalUploadResponse)
async def upload_local_video(file: UploadFile = File(...)):
    """Uploads a local video and returns upload metadata."""
    metadata = await UploadService.process_local_upload(file)
    
    return LocalUploadResponse(
        success=True,
        job_id=metadata.job_id,
        message="Video uploaded successfully.",
        data={
            "filename": metadata.original_filename,
            "file_size": metadata.file_size,
            "upload_source": metadata.upload_source
        }
    )

@router.post("/youtube", response_model=YouTubeUploadResponse)
async def upload_youtube_video(request: YouTubeUploadRequest = Body(...)):
    """Downloads a YouTube video and returns upload metadata."""
    metadata = await DownloaderService.process_youtube_upload(request.url)
    
    return YouTubeUploadResponse(
        success=True,
        job_id=metadata["job_id"],
        message="Video downloaded successfully.",
        data={
            "title": metadata["original_filename"],
            "file_size": metadata["file_size"],
            "upload_source": metadata["upload_source"]
        }
    )
