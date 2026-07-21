import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.summary.validator import SummaryValidator
from app.modules.summary.generator import SummaryGenerator
from app.modules.summary.merger import SummaryMerger
from app.modules.summary.formatter import SummaryFormatter
from app.modules.summary.metadata import MetadataGenerator
from app.modules.summary.schemas import SummaryResponse
from app.modules.summary.exceptions import SummaryError

class SummaryService:
    """Orchestrates the AI Summary Generation pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        base_path = Path(settings.PROCESSED_DIR) / job_id / "summary"
        base_path.mkdir(parents=True, exist_ok=True)
        return {
            "base": base_path,
            "json": base_path / "summary.json",
            "executive": base_path / "executive_summary.md",
            "detailed": base_path / "detailed_summary.md",
            "bullet": base_path / "bullet_summary.md",
            "metadata": base_path / "metadata.json"
        }

    @staticmethod
    def process_job(job_id: str) -> SummaryResponse:
        logger.info(f"Starting Summary Generation Pipeline for job {job_id}")
        start_time = time.time()
        
        try:
            job_dir = Path(settings.PROCESSED_DIR) / job_id
            chunks_path = job_dir / "chunks" / "chunks.json"
            
            # 1. Validate
            SummaryValidator.validate(str(chunks_path))
            
            # 2. Setup Directories
            dirs = SummaryService.ensure_directories(job_id)
            
            # 3. Generate Chunk Summaries (via LLM Orchestrator)
            chunk_summaries = SummaryGenerator.generate_chunk_summaries(job_id)
            num_chunks = len(chunk_summaries)
            
            # 4. Merge Summaries
            summary_json, tokens = SummaryMerger.merge(job_id, chunk_summaries)
            
            # 5. Format & Save
            SummaryFormatter.format(summary_json, dirs)
            
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
                
            logger.info(f"Successfully built AI Summary for job {job_id}")
            
            return SummaryResponse(
                success=True,
                job_id=job_id,
                message="Summary generation completed successfully.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"Summary generation failed for job {job_id}: {str(e)}")
            raise SummaryError(details={"error": str(e)})
