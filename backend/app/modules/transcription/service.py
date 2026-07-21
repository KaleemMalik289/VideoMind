import os
import json
import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.transcription.validator import AudioValidator
from app.modules.transcription.transcriber import AudioTranscriber
from app.modules.transcription.parser import TranscriptParser
from app.modules.transcription.formatter import TranscriptFormatter
from app.modules.transcription.metadata import MetadataGenerator
from app.modules.transcription.schemas import TranscriptionResponse, TranscriptJSON
from app.modules.transcription.exceptions import TranscriptionError

class TranscriptionService:
    """Orchestrates the Speech Transcription pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        """Ensures the transcript output directories exist."""
        base_path = Path(settings.PROCESSED_DIR) / job_id / "transcript"
        base_path.mkdir(parents=True, exist_ok=True)
        return {
            "base": base_path,
            "json": base_path / "transcript.json",
            "text": base_path / "transcript.txt",
            "metadata": base_path / "metadata.json"
        }

    @staticmethod
    def get_audio_duration(job_id: str) -> float:
        """Reads duration from audio metadata."""
        metadata_path = Path(settings.PROCESSED_DIR) / job_id / "audio" / "metadata.json"
        try:
            with open(metadata_path, "r") as f:
                data = json.load(f)
                return float(data.get("duration", 0.0))
        except Exception:
            return 0.0

    @staticmethod
    def process_job(job_id: str) -> TranscriptionResponse:
        """Runs the entire transcription pipeline for a job."""
        logger.info(f"Starting Speech Transcription Pipeline for job {job_id}")
        start_time = time.time()
        
        try:
            audio_path = Path(settings.PROCESSED_DIR) / job_id / "audio" / "processed_audio.wav"
            audio_path_str = str(audio_path)
            
            # 1. Validate
            AudioValidator.validate(audio_path_str)
            
            # 2. Setup Directories
            dirs = TranscriptionService.ensure_directories(job_id)
            
            # 3. Transcribe Audio
            raw_segments, info = AudioTranscriber.transcribe(audio_path_str)
            
            # 4. Parse & Clean Segments
            # (Note: raw_segments is an iterator, list() realizes it)
            parsed_segments = TranscriptParser.parse_segments(list(raw_segments))
            
            # Get precise audio duration
            audio_duration = TranscriptionService.get_audio_duration(job_id)
            
            transcript_json = TranscriptJSON(
                job_id=job_id,
                language=info.language,
                duration=audio_duration,
                segments=parsed_segments
            )
            
            # 5. Format & Save
            TranscriptFormatter.save_json(transcript_json, dirs["json"])
            TranscriptFormatter.save_text(transcript_json, dirs["text"])
            
            # 6. Generate Metadata
            processing_time = time.time() - start_time
            metadata = MetadataGenerator.generate(job_id, transcript_json, audio_duration, processing_time)
            
            with open(dirs["metadata"], "w", encoding="utf-8") as f:
                f.write(metadata.model_dump_json(indent=2))
                
            logger.info(f"Successfully completed Transcription Pipeline for job {job_id}")
            
            return TranscriptionResponse(
                success=True,
                job_id=job_id,
                message="Speech transcription completed successfully.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"Transcription Pipeline failed for job {job_id}: {str(e)}")
            raise TranscriptionError(details={"error": str(e)})
