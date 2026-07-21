from app.modules.code_extraction.schemas import CodeMetadata
from app.core.settings import settings

class MetadataGenerator:
    @staticmethod
    def generate(job_id: str, num_chunks: int, num_files: int, syntax_valid: bool, tokens: int, processing_time: float) -> CodeMetadata:
        return CodeMetadata(
            job_id=job_id,
            num_chunks_processed=num_chunks,
            num_files_extracted=num_files,
            syntax_valid=syntax_valid,
            model_used=settings.LLM_MODEL,
            total_tokens=tokens,
            processing_duration_sec=round(processing_time, 2)
        )
