import subprocess
import json
import os
from loguru import logger
from app.core.settings import settings
from app.modules.audio.schemas import AudioMetadata
from app.modules.audio.exceptions import AudioExtractionError

class MetadataGenerator:
    """Generates precise audio metadata using ffprobe."""
    
    @staticmethod
    def generate(job_id: str, audio_path: str) -> AudioMetadata:
        logger.info(f"Generating metadata for {audio_path}")
        
        cmd = [
            settings.FFPROBE_PATH,
            "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=codec_name,sample_rate,channels,duration",
            "-of", "json",
            audio_path
        ]
        
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            info = json.loads(result.stdout)
            
            stream = info.get("streams", [{}])[0]
            
            # Duration can sometimes be missing in streams, fallback to format
            duration = float(stream.get("duration", 0.0))
            if duration == 0.0:
                cmd_fmt = [
                    settings.FFPROBE_PATH,
                    "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "json",
                    audio_path
                ]
                res2 = subprocess.run(cmd_fmt, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                info2 = json.loads(res2.stdout)
                duration = float(info2.get("format", {}).get("duration", 0.0))
            
            file_size = os.path.getsize(audio_path)
            
            return AudioMetadata(
                job_id=job_id,
                duration=duration,
                sample_rate=int(stream.get("sample_rate", 0)),
                channels=int(stream.get("channels", 0)),
                codec=stream.get("codec_name", "unknown"),
                file_size=file_size
            )
            
        except subprocess.CalledProcessError as e:
            logger.error(f"ffprobe metadata extraction failed: {e.stderr}")
            raise AudioExtractionError(details={"error": "Failed to generate metadata via ffprobe."})
        except Exception as e:
            logger.error(f"Error parsing metadata: {str(e)}")
            raise AudioExtractionError(details={"error": str(e)})
