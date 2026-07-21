import subprocess
from loguru import logger
from app.core.settings import settings
from app.modules.audio.exceptions import AudioExtractionError

class AudioConverter:
    """Handles codec and format conversions."""
    
    @staticmethod
    def convert_format(input_path: str, output_path: str) -> str:
        """Converts audio to the desired codec (e.g., PCM 16-bit)."""
        logger.info(f"Converting audio format for {input_path}")
        cmd = [
            settings.FFMPEG_PATH,
            "-y", "-i", input_path,
            "-acodec", settings.AUDIO_BIT_DEPTH,
            output_path
        ]
        
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg conversion failed: {e.stderr.decode('utf-8', errors='ignore')}")
            raise AudioExtractionError(details={"error": "FFmpeg format conversion failed."})
