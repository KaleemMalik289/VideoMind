import os
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.audio.validator import VideoAudioValidator
from app.modules.audio.extractor import AudioExtractor
from app.modules.audio.converter import AudioConverter
from app.modules.audio.normalizer import AudioNormalizer
from app.modules.audio.metadata import MetadataGenerator
from app.modules.audio.schemas import AudioResponse
from app.modules.audio.exceptions import AudioExtractionError

class AudioService:
    """Orchestrates the Audio Extraction pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> Path:
        """Ensures the audio output directory exists."""
        audio_dir = Path(settings.PROCESSED_DIR) / job_id / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        return audio_dir

    @staticmethod
    def process_job(job_id: str, video_path: str) -> AudioResponse:
        """Runs the entire audio pipeline for a job."""
        logger.info(f"Starting Audio Extraction Pipeline for job {job_id}")
        
        try:
            # 1. Validate
            VideoAudioValidator.validate(video_path)
            
            # 2. Setup Directories
            audio_dir = AudioService.ensure_directories(job_id)
            original_audio_path = str(audio_dir / "original_audio.wav")
            processed_audio_path = str(audio_dir / "processed_audio.wav")
            metadata_path = audio_dir / "metadata.json"
            
            # 3. Extract Original Audio
            AudioExtractor.extract(video_path, original_audio_path)
            
            # 4. Convert Format & Normalize
            # Chaining the independent components as per design
            temp_audio_path = str(audio_dir / "temp_audio.wav")
            AudioConverter.convert_format(original_audio_path, temp_audio_path)
            AudioNormalizer.normalize(temp_audio_path, processed_audio_path)
            
            # Cleanup temp file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            # 5. Generate Metadata
            metadata = MetadataGenerator.generate(job_id, processed_audio_path)
            
            with open(metadata_path, "w", encoding="utf-8") as f:
                f.write(metadata.model_dump_json(indent=2))
                
            logger.info(f"Successfully completed Audio Pipeline for job {job_id}")
            
            return AudioResponse(
                success=True,
                job_id=job_id,
                message="Audio extraction completed successfully.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"Audio Pipeline failed for job {job_id}: {str(e)}")
            raise AudioExtractionError(details={"error": str(e)})
