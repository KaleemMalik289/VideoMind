from app.core.settings import settings

class TimelineSynchronizer:
    """Finds the optimal timestamp match between OCR frames and Transcript segments."""
    
    @staticmethod
    def find_nearest_segment(ocr_timestamp: float, transcript_segments: list) -> dict:
        """
        Finds the transcript segment whose [start, end] window is closest to the OCR frame.
        Returns the segment dict if it falls within TIMELINE_SYNC_WINDOW, else None.
        """
        best_segment = None
        min_distance = float('inf')
        window = settings.TIMELINE_SYNC_WINDOW
        
        for seg in transcript_segments:
            start = seg.get("start", 0.0)
            end = seg.get("end", 0.0)
            
            # If the frame lands exactly inside the transcript segment
            if start <= ocr_timestamp <= end:
                return seg
                
            # Otherwise, calculate distance to nearest edge
            dist_to_start = abs(ocr_timestamp - start)
            dist_to_end = abs(ocr_timestamp - end)
            min_edge_dist = min(dist_to_start, dist_to_end)
            
            if min_edge_dist < min_distance and min_edge_dist <= window:
                min_distance = min_edge_dist
                best_segment = seg
                
        return best_segment
