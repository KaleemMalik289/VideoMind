import os
import re
from pathlib import Path
import yt_dlp
from app.modules.downloader.exceptions import InvalidYouTubeURLError, DownloadFailedError
from app.modules.upload.storage import UploadStorage
from loguru import logger
from typing import Tuple

class YouTubeDownloader:
    """Handles downloading and validating videos from YouTube."""
    
    YOUTUBE_URL_REGEX = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    
    @staticmethod
    def validate_url(url: str) -> None:
        if not re.match(YouTubeDownloader.YOUTUBE_URL_REGEX, url):
            raise InvalidYouTubeURLError()
            
    @staticmethod
    async def download_video(url: str, job_id: str) -> Tuple[str, str, int, str]:
        """Downloads the video to the job's directory and returns file details."""
        original_dir = UploadStorage.create_job_directory(job_id)
        
        # Download best quality up to 1080p, merged into mp4
        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(original_dir / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            logger.info(f"Starting YouTube download for {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                
                # Retrieve the filename downloaded
                filename = ydl.prepare_filename(info_dict)
                if info_dict.get('requested_formats'):
                    # if merged, it forces mp4
                    filename = os.path.splitext(filename)[0] + '.mp4'
                
                file_path = Path(filename)
                absolute_path = str(file_path.resolve())
                relative_path = str(file_path.relative_to(Path.cwd()))
                file_size = os.path.getsize(file_path)
                
                video_title = info_dict.get('title', 'youtube_video')
                
                logger.info(f"Successfully downloaded YouTube video for job {job_id}.")
                return absolute_path, relative_path, file_size, video_title
                
        except Exception as e:
            logger.error(f"YouTube download failed for job {job_id}: {str(e)}")
            raise DownloadFailedError(details={"error": str(e)})
