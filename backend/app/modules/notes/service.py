import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.notes.validator import NotesValidator
from app.modules.notes.generator import NotesGenerator
from app.modules.notes.merger import NotesMerger
from app.modules.notes.formatter import NotesFormatter
from app.modules.notes.metadata import MetadataGenerator
from app.modules.notes.schemas import NotesResponse
from app.modules.notes.exceptions import NotesError

class NotesService:
    """Orchestrates the Smart Notes Generation pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        base_path = Path(settings.PROCESSED_DIR) / job_id / "notes"
        base_path.mkdir(parents=True, exist_ok=True)
        return {
            "base": base_path,
            "json": base_path / "notes.json",
            "markdown": base_path / "notes.md",
            "metadata": base_path / "metadata.json"
        }

    @staticmethod
    def process_job(job_id: str) -> NotesResponse:
        logger.info(f"Starting Smart Notes Generation Pipeline for job {job_id}")
        start_time = time.time()
        
        try:
            job_dir = Path(settings.PROCESSED_DIR) / job_id
            chunks_path = job_dir / "chunks" / "chunks.json"
            
            # 1. Validate
            NotesValidator.validate(str(chunks_path))
            
            # 2. Setup Directories
            dirs = NotesService.ensure_directories(job_id)
            
            # 3. Generate Chunk Notes (via LLM Orchestrator)
            chunk_notes = NotesGenerator.generate_chunk_notes(job_id)
            num_chunks = len(chunk_notes)
            
            # 4. Merge Notes
            notes_json, tokens = NotesMerger.merge(job_id, chunk_notes)
            
            # 5. Format & Save
            NotesFormatter.format(notes_json, dirs)
            
            # 6. Generate Metadata
            processing_time = time.time() - start_time
            metadata = MetadataGenerator.generate(
                job_id=job_id,
                num_chunks=num_chunks,
                tokens=tokens,
                processing_time=processing_time
            )
            
            with open(dirs["metadata"], "w", encoding="utf-8") as f:
                f.write(metadata.model_dump_json(indent=2))
                
            logger.info(f"Successfully generated Smart Notes for job {job_id}")
            
            return NotesResponse(
                success=True,
                job_id=job_id,
                message="Smart Notes generation completed successfully.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"Smart Notes generation failed for job {job_id}: {str(e)}")
            raise NotesError(details={"error": str(e)})
