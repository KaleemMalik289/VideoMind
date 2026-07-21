from app.modules.summary.schemas import SummaryMetadata
from app.core.settings import settings

class MetadataGenerator:
    @staticmethod
    def generate(job_id: str, num_chunks: int, tokens: int, processing_time: float) -> SummaryMetadata:
        return SummaryMetadata(
            job_id=job_id,
            num_chunks_processed=num_chunks,
            model_used=settings.LLM_MODEL,
            total_tokens=tokens,
            processing_duration_sec=round(processing_time, 2)
        )
