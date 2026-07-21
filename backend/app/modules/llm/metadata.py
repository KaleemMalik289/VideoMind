from app.modules.llm.schemas import LLMMetadata, LLMJobResponse
import time

class MetadataGenerator:
    """Generates metadata for LLM jobs."""
    
    @staticmethod
    def generate(job_id: str, provider: str, model: str, response: LLMJobResponse, processing_time: float) -> LLMMetadata:
        total_tokens = sum(r.tokens_used for r in response.responses)
        
        return LLMMetadata(
            job_id=job_id,
            provider=provider,
            model=model,
            total_tokens=total_tokens,
            processing_duration_sec=round(processing_time, 2),
            num_chunks=len(response.responses)
        )
