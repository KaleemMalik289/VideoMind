import subprocess
from loguru import logger
from app.core.settings import settings
from app.modules.audio.exceptions import AudioExtractionError

class AudioExtractor:
    """Responsible for ripping the raw audio track from a video."""
    
    @staticmethod
    def extract(video_path: str, output_path: str) -> str:
        logger.info(f"Extracting raw audio from {video_path}")
        cmd = [
            settings.FFMPEG_PATH,
            "-y", "-i", video_path,
            "-vn",  # no video
            output_path
        ]
        
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg extraction failed: {e.stderr.decode('utf-8', errors='ignore')}")
            raise AudioExtractionError(details={"error": "FFmpeg extraction failed."})
