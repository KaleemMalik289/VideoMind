import cv2
import numpy as np

class DenoiseFilter:
    @staticmethod
    def apply(img: np.ndarray) -> np.ndarray:
        # Bilateral filter is highly effective at noise removal while preserving edges
        return cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
