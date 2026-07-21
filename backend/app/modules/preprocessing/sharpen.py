import cv2
import numpy as np

class SharpenFilter:
    @staticmethod
    def apply(img: np.ndarray) -> np.ndarray:
        # Create a laplacian/unsharp mask kernel
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        return cv2.filter2D(img, -1, kernel)
