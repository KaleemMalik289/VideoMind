import json
from pathlib import Path
from typing import List
from app.modules.llm.schemas import LLMChunkResponse, LLMJobResponse

class ResponseAggregator:
    """Aggregates individual chunk responses into a single merged structure."""
    
    @staticmethod
    def aggregate(job_id: str, chunk_responses: List[LLMChunkResponse], merged_path: Path) -> LLMJobResponse:
        # Ensure ordered by chunk_id
        chunk_responses.sort(key=lambda x: x.chunk_id)
        
        job_response = LLMJobResponse(
            job_id=job_id,
            responses=chunk_responses
        )
        
        with open(merged_path, "w", encoding="utf-8") as f:
            f.write(job_response.model_dump_json(indent=2))
            
        return job_response
