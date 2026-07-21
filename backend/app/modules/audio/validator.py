import os
import subprocess
import json
from loguru import logger
from app.core.settings import settings
from app.modules.audio.exceptions import AudioValidationError

class VideoAudioValidator:
    """Validates that a video file exists and actually contains an audio stream."""
    
    @staticmethod
    def validate(video_path: str) -> None:
        if not os.path.exists(video_path):
            logger.error(f"Missing video file: {video_path}")
            raise AudioValidationError(details={"path": video_path, "reason": "Missing file"})
            
        if os.path.getsize(video_path) == 0:
            logger.error(f"Empty video file: {video_path}")
            raise AudioValidationError(details={"path": video_path, "reason": "Empty file"})
            
        # Use ffprobe to check for audio streams
        try:
            cmd = [
                settings.FFPROBE_PATH,
                "-v", "error",
                "-select_streams", "a",
                "-show_entries", "stream=codec_type",
                "-of", "json",
                video_path
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            info = json.loads(result.stdout)
            
            if not info.get("streams") or len(info["streams"]) == 0:
                logger.error(f"No audio stream found in video: {video_path}")
                raise AudioValidationError(details={"path": video_path, "reason": "No audio stream present"})
                
        except subprocess.CalledProcessError as e:
            logger.error(f"ffprobe failed to read video streams for {video_path}: {e.stderr}")
            raise AudioValidationError(details={"path": video_path, "reason": "Unsupported format or corrupted file"})
        except AudioValidationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error validating audio stream for {video_path}: {str(e)}")
            raise AudioValidationError(details={"path": video_path, "reason": str(e)})
