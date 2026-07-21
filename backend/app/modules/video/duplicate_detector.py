import imagehash
from PIL import Image
from loguru import logger
from app.core.settings import settings

class DuplicateDetector:
    """Removes visually similar frames using Perceptual Hashing."""
    
    @staticmethod
    def filter_duplicates(frame_paths: list[str]) -> list[str]:
        """Filters out frames that are too visually similar to previous frames."""
        logger.info(f"Starting duplicate detection for {len(frame_paths)} frames")
        
        if not frame_paths:
            return []
            
        unique_paths = []
        previous_hash = None
        
        # The threshold for imagehash difference. 
        # A difference of 0 means identical. Usually difference < 5 is very similar.
        # Translating FRAME_SIMILARITY_THRESHOLD (0.95) to hash difference:
        # pHash length is 64 bits. 5% difference is roughly 3 bits.
        similarity_threshold_bits = int((1.0 - settings.FRAME_SIMILARITY_THRESHOLD) * 64)
        if similarity_threshold_bits < 1:
            similarity_threshold_bits = 1
            
        for path in frame_paths:
            try:
                img = Image.open(path)
                current_hash = imagehash.phash(img)
                
                if previous_hash is None:
                    unique_paths.append(path)
                    previous_hash = current_hash
                else:
                    diff = current_hash - previous_hash
                    if diff > similarity_threshold_bits:
                        unique_paths.append(path)
                        previous_hash = current_hash
                        
            except Exception as e:
                logger.error(f"Error hashing image {path}: {str(e)}")
                # include it if it fails to hash just to be safe
                unique_paths.append(path)
                
        logger.info(f"Filtered down to {len(unique_paths)} unique frames.")
        return unique_paths
