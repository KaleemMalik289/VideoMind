import os
import json
import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.llm.validator import LLMValidator
from app.modules.llm.orchestrator import ProviderFactory
from app.modules.llm.chunk_processor import ChunkProcessor
from app.modules.llm.aggregator import ResponseAggregator
from app.modules.llm.metadata import MetadataGenerator
from app.modules.llm.schemas import FinalResponse
from app.modules.llm.exceptions import LLMError

class LLMService:
    """Central AI engine orchestration pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        base_path = Path(settings.PROCESSED_DIR) / job_id / "llm"
        raw_dir = base_path / "raw"
        merged_dir = base_path / "merged"
        
        raw_dir.mkdir(parents=True, exist_ok=True)
        merged_dir.mkdir(parents=True, exist_ok=True)
        
        return {
            "base": base_path,
            "raw": raw_dir,
            "merged": merged_dir,
            "merged_file": merged_dir / "merged_response.json",
            "metadata": base_path / "metadata.json"
        }

    @staticmethod
    def process_job(job_id: str, system_prompt: str, user_prompt_template: str) -> FinalResponse:
        logger.info(f"Starting LLM Orchestration Pipeline for job {job_id}")
        start_time = time.time()
        
        try:
            job_dir = Path(settings.PROCESSED_DIR) / job_id
            chunks_path = job_dir / "chunks" / "chunks.json"
            
            # 1. Validate
            LLMValidator.validate(str(chunks_path))
            
            # 2. Setup Directories
            dirs = LLMService.ensure_directories(job_id)
            
            # 3. Load Chunks
            with open(chunks_path, "r", encoding="utf-8") as f:
                c_data = json.load(f)
                chunks = c_data.get("chunks", [])
                
            if not chunks:
                logger.warning(f"No semantic chunks found for job {job_id}")
                raise LLMError(details={"reason": "Empty chunks array."})
                
            # 4. Initialize Provider
            provider = ProviderFactory.get_provider()
            
            # 5. Process Chunks
            processor = ChunkProcessor(provider=provider, raw_dir=dirs["raw"])
            chunk_responses = []
            
            for chunk in chunks:
                resp = processor.process(chunk, system_prompt, user_prompt_template)
                chunk_responses.append(resp)
                
            # 6. Aggregate
            job_response = ResponseAggregator.aggregate(job_id, chunk_responses, dirs["merged_file"])
            
            # 7. Generate Metadata
            processing_time = time.time() - start_time
            metadata = MetadataGenerator.generate(
                job_id=job_id,
                provider=provider.__class__.__name__,
                model=getattr(provider, "model", "unknown"),
                response=job_response,
                processing_time=processing_time
            )
            
            with open(dirs["metadata"], "w", encoding="utf-8") as f:
                f.write(metadata.model_dump_json(indent=2))
                
            logger.info(f"Successfully processed all chunks for job {job_id}")
            
            return FinalResponse(
                success=True,
                job_id=job_id,
                message="LLM processing completed successfully.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"LLM processing failed for job {job_id}: {str(e)}")
            raise LLMError(details={"error": str(e)})
