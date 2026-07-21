from app.modules.timeline.schemas import TimelineMetadata
import time

class MetadataGenerator:
    """Generates timeline metadata."""
    
    @staticmethod
    def generate(job_id: str, num_entries: int, ocr_merged: int, transcript_merged: int, processing_time: float) -> TimelineMetadata:
        return TimelineMetadata(
            job_id=job_id,
            num_entries=num_entries,
            ocr_segments_merged=ocr_merged,
            transcript_segments_merged=transcript_merged,
            processing_duration_sec=round(processing_time, 2)
        )
