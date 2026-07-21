import os
import json
import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.timeline.validator import TimelineValidator
from app.modules.timeline.builder import TimelineBuilder
from app.modules.timeline.formatter import TimelineFormatter
from app.modules.timeline.metadata import MetadataGenerator
from app.modules.timeline.schemas import TimelineResponse, TimelineJSON
from app.modules.timeline.exceptions import TimelineError

class TimelineService:
    """Orchestrates the Multimodal Timeline Builder."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        base_path = Path(settings.PROCESSED_DIR) / job_id / "timeline"
        base_path.mkdir(parents=True, exist_ok=True)
        return {
            "base": base_path,
            "json": base_path / "timeline.json",
            "text": base_path / "timeline.txt",
            "metadata": base_path / "metadata.json"
        }

    @staticmethod
    def process_job(job_id: str) -> TimelineResponse:
        logger.info(f"Starting Timeline Generation Pipeline for job {job_id}")
        start_time = time.time()
        
        try:
            job_dir = Path(settings.PROCESSED_DIR) / job_id
            ocr_dir = job_dir / "ocr" / "json"
            transcript_path = job_dir / "transcript" / "transcript.json"
            
            # 1. Validate
            TimelineValidator.validate(str(ocr_dir), str(transcript_path))
            
            # 2. Setup Directories
            dirs = TimelineService.ensure_directories(job_id)
            
            # 3. Load Datasets
            # Load Transcript
            with open(transcript_path, "r", encoding="utf-8") as f:
                t_data = json.load(f)
                transcript_segments = t_data.get("segments", [])
                
            # Load OCR
            ocr_frames = []
            if os.path.exists(ocr_dir):
                for filename in sorted(os.listdir(ocr_dir)):
                    if filename.endswith(".json"):
                        with open(ocr_dir / filename, "r", encoding="utf-8") as f:
                            ocr_frames.append(json.load(f))
                            
            # 4. Build Timeline
            entries, ocr_count, transcript_count = TimelineBuilder.build(ocr_frames, transcript_segments)
            
            timeline_json = TimelineJSON(
                job_id=job_id,
                entries=entries
            )
            
            # 5. Format & Save
            TimelineFormatter.save_json(timeline_json, dirs["json"])
            TimelineFormatter.save_text(timeline_json, dirs["text"])
            
            # 6. Generate Metadata
            processing_time = time.time() - start_time
            metadata = MetadataGenerator.generate(
                job_id=job_id,
                num_entries=len(entries),
                ocr_merged=ocr_count,
                transcript_merged=transcript_count,
                processing_time=processing_time
            )
            
            with open(dirs["metadata"], "w", encoding="utf-8") as f:
                f.write(metadata.model_dump_json(indent=2))
                
            logger.info(f"Successfully built Multimodal Timeline for job {job_id}")
            
            return TimelineResponse(
                success=True,
                job_id=job_id,
                message="Timeline built successfully.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"Timeline generation failed for job {job_id}: {str(e)}")
            raise TimelineError(details={"error": str(e)})
