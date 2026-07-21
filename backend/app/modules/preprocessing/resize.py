import cv2
import numpy as np

class ResizeFilter:
    @staticmethod
    def apply(img: np.ndarray, target_width: int, target_height: int) -> np.ndarray:
        h, w = img.shape[:2]
        
        # Calculate aspect ratio
        aspect = w / h
        target_aspect = target_width / target_height
        
        if aspect > target_aspect:
            # Image is wider than target ratio
            new_w = target_width
            new_h = int(target_width / aspect)
        else:
            # Image is taller than target ratio
            new_h = target_height
            new_w = int(target_height * aspect)
            
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        return resized
