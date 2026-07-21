from app.modules.chunking.schemas import ChunkMetadata
import time

class MetadataGenerator:
    @staticmethod
    def generate(job_id: str, chunks: list, processing_time: float) -> ChunkMetadata:
        num_chunks = len(chunks)
        if num_chunks == 0:
            return ChunkMetadata(
                job_id=job_id,
                num_chunks=0,
                avg_chunk_size_sec=0.0,
                avg_token_count=0.0,
                processing_duration_sec=round(processing_time, 2)
            )
            
        avg_dur = sum((c.end - c.start) for c in chunks) / num_chunks
        avg_tok = sum(c.estimated_tokens for c in chunks) / num_chunks
        
        return ChunkMetadata(
            job_id=job_id,
            num_chunks=num_chunks,
            avg_chunk_size_sec=round(avg_dur, 2),
            avg_token_count=round(avg_tok, 2),
            processing_duration_sec=round(processing_time, 2)
        )
