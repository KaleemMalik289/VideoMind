import cv2
import numpy as np

class ThresholdFilter:
    @staticmethod
    def apply(img: np.ndarray) -> np.ndarray:
        # Convert to grayscale first
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
            
        # Apply Otsu's thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary
