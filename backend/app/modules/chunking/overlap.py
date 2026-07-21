from app.core.settings import settings

class OverlapManager:
    """Manages the carry-over of timeline context across semantic chunk boundaries."""
    
    @staticmethod
    def get_overlap_entries(timeline_entries: list, chunk_end_time: float) -> list:
        """
        Returns timeline entries from the end of the current chunk that should
        be carried over into the start of the NEXT chunk to preserve context.
        """
        if not settings.ENABLE_CONTEXT_OVERLAP or not timeline_entries:
            return []
            
        overlap_start = chunk_end_time - settings.CHUNK_OVERLAP_SECONDS
        
        # Find entries that overlap this time window
        overlap = []
        for entry in reversed(timeline_entries):
            # entry ends after overlap_start means it intersects the overlap window
            if entry.get("end", 0.0) >= overlap_start:
                overlap.insert(0, entry)
            else:
                break # We've gone past the overlap window
                
        return overlap
