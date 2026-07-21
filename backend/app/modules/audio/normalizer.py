import subprocess
from loguru import logger
from app.core.settings import settings
from app.modules.audio.exceptions import AudioExtractionError

class AudioNormalizer:
    """Handles audio normalization (sample rate, channels, volume)."""
    
    @staticmethod
    def normalize(input_path: str, output_path: str) -> str:
        """Applies 16kHz resampling, Mono downmixing, and loudnorm volume normalization."""
        logger.info(f"Normalizing audio for {input_path}")
        cmd = [
            settings.FFMPEG_PATH,
            "-y", "-i", input_path,
            "-ar", str(settings.AUDIO_SAMPLE_RATE),
            "-ac", str(settings.AUDIO_CHANNELS),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", # standard EBU R128 loudnorm
            output_path
        ]
        
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg normalization failed: {e.stderr.decode('utf-8', errors='ignore')}")
            raise AudioExtractionError(details={"error": "FFmpeg normalization failed."})
