import cv2
import numpy as np
from loguru import logger
from app.core.settings import settings
from app.modules.preprocessing.resize import ResizeFilter
from app.modules.preprocessing.denoise import DenoiseFilter
from app.modules.preprocessing.sharpen import SharpenFilter
from app.modules.preprocessing.contrast import ContrastFilter
from app.modules.preprocessing.threshold import ThresholdFilter
from app.modules.preprocessing.rotation import RotationFilter

class PreprocessingPipeline:
    """Dynamically applies enabled preprocessing filters to an image."""
    
    @staticmethod
    def process_image(img: np.ndarray) -> tuple[np.ndarray, list[str]]:
        applied_operations = []
        processed_img = img.copy()
        
        if settings.PREPROCESS_ENABLE_RESIZE:
            processed_img = ResizeFilter.apply(
                processed_img, 
                settings.PREPROCESS_IMAGE_WIDTH, 
                settings.PREPROCESS_IMAGE_HEIGHT
            )
            applied_operations.append("resize")
            
        if settings.PREPROCESS_ENABLE_DENOISE:
            processed_img = DenoiseFilter.apply(processed_img)
            applied_operations.append("denoise")
            
        if settings.PREPROCESS_ENABLE_SHARPEN:
            processed_img = SharpenFilter.apply(processed_img)
            applied_operations.append("sharpen")
            
        if settings.PREPROCESS_ENABLE_CONTRAST:
            processed_img = ContrastFilter.apply(processed_img, settings.PREPROCESS_CLAHE_CLIP_LIMIT)
            applied_operations.append("contrast")
            
        if settings.PREPROCESS_ENABLE_THRESHOLD:
            processed_img = ThresholdFilter.apply(processed_img)
            applied_operations.append("threshold")
            
        if settings.PREPROCESS_ENABLE_ROTATION:
            processed_img = RotationFilter.apply(processed_img)
            applied_operations.append("rotation")
            
        return processed_img, applied_operations
