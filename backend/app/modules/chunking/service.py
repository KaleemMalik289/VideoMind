import json
import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.chunking.validator import TimelineValidator
from app.modules.chunking.builder import ChunkBuilder
from app.modules.chunking.formatter import ChunkFormatter
from app.modules.chunking.metadata import MetadataGenerator
from app.modules.chunking.schemas import ChunkResponse, ChunkJSON
from app.modules.chunking.exceptions import ChunkingError

class ChunkingService:
    """Orchestrates the Semantic Chunking pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        base_path = Path(settings.PROCESSED_DIR) / job_id / "chunks"
        base_path.mkdir(parents=True, exist_ok=True)
        return {
            "base": base_path,
            "json": base_path / "chunks.json",
            "text": base_path / "chunks.txt",
            "metadata": base_path / "metadata.json"
        }

    @staticmethod
    def process_job(job_id: str) -> ChunkResponse:
        logger.info(f"Starting Semantic Chunking Pipeline for job {job_id}")
        start_time = time.time()
        
        try:
            job_dir = Path(settings.PROCESSED_DIR) / job_id
            timeline_path = job_dir / "timeline" / "timeline.json"
            
            # 1. Validate
            TimelineValidator.validate(str(timeline_path))
            
            # 2. Setup Directories
            dirs = ChunkingService.ensure_directories(job_id)
            
            # 3. Load Datasets
            with open(timeline_path, "r", encoding="utf-8") as f:
                t_data = json.load(f)
                timeline_entries = t_data.get("entries", [])
                
            # 4. Build Chunks
            chunks = ChunkBuilder.build(timeline_entries)
            
            chunk_json = ChunkJSON(
                job_id=job_id,
                chunks=chunks
            )
            
            # 5. Format & Save
            ChunkFormatter.save_json(chunk_json, dirs["json"])
            ChunkFormatter.save_text(chunk_json, dirs["text"])
            
            # 6. Generate Metadata
            processing_time = time.time() - start_time
            metadata = MetadataGenerator.generate(
                job_id=job_id,
                chunks=chunks,
                processing_time=processing_time
            )
            
            with open(dirs["metadata"], "w", encoding="utf-8") as f:
                f.write(metadata.model_dump_json(indent=2))
                
            logger.info(f"Successfully built Semantic Chunks for job {job_id}")
            
            return ChunkResponse(
                success=True,
                job_id=job_id,
                message="Semantic chunking completed successfully.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"Semantic chunking failed for job {job_id}: {str(e)}")
            raise ChunkingError(details={"error": str(e)})
