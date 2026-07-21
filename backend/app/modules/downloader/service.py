from datetime import datetime, timezone
from app.modules.downloader.youtube import YouTubeDownloader
from app.modules.upload.storage import UploadStorage
from app.modules.upload.schemas import UploadMetadata
from loguru import logger

class DownloaderService:
    """Orchestrates the YouTube download pipeline."""
    
    @staticmethod
    async def process_youtube_upload(url: str) -> dict:
        """Handles validation, downloading, and metadata generation for a YouTube upload."""
        logger.info(f"Processing YouTube URL: {url}")
        
        # 1. Validate URL
        YouTubeDownloader.validate_url(url)
        
        # 2. Generate Job ID
        job_id = UploadStorage.generate_job_id()
        
        # 3. Download
        absolute_path, relative_path, file_size, title = await YouTubeDownloader.download_video(
            url=url, 
            job_id=job_id
        )
        
        # 4. Extract Metadata
        import os
        filename = os.path.basename(absolute_path)
        
        metadata = UploadMetadata(
            job_id=job_id,
            original_filename=title,
            stored_filename=filename,
            upload_timestamp=datetime.now(timezone.utc),
            file_size=file_size,
            file_extension=filename.split(".")[-1] if "." in filename else "",
            mime_type="video/mp4", # Enforced by yt-dlp config
            upload_source="youtube",
            absolute_storage_path=absolute_path,
            relative_storage_path=relative_path
        )
        
        logger.info(f"Completed YouTube download process for job {job_id}.")
        return metadata.model_dump()
