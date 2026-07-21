import cv2
import os
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.preprocessing.validator import ImageValidator
from app.modules.preprocessing.pipeline import PreprocessingPipeline
from app.modules.preprocessing.schemas import PreprocessingMetadata
from app.modules.preprocessing.exceptions import ImageProcessingError

class ImageProcessor:
    """Handles file I/O for a single frame through the preprocessing pipeline."""
    
    @staticmethod
    def process_frame(frame_id: int, original_path: str, output_dir: Path) -> PreprocessingMetadata:
        try:
            # 1. Validate
            ImageValidator.validate(original_path)
            
            # 2. Read image
            img = cv2.imread(original_path)
            if img is None:
                raise ImageProcessingError(f"Failed to read image {original_path} with OpenCV.")
                
            # 3. Apply pipeline
            processed_img, operations = PreprocessingPipeline.process_image(img)
            
            # 4. Save processed image
            filename = os.path.basename(original_path)
            processed_path = output_dir / filename
            
            # If Thresholding is enabled, it's grayscale/binary, so no format issues.
            cv2.imwrite(str(processed_path), processed_img, [cv2.IMWRITE_JPEG_QUALITY, settings.PREPROCESS_OUTPUT_QUALITY])
            
            # 5. Return Metadata
            return PreprocessingMetadata(
                frame_id=frame_id,
                original_image=str(original_path),
                processed_image=str(processed_path),
                operations=operations
            )
            
        except Exception as e:
            logger.error(f"Error processing frame {frame_id} from {original_path}: {str(e)}")
            raise ImageProcessingError(details={"error": str(e), "path": original_path})
