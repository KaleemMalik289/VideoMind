import cv2
import numpy as np

class RotationFilter:
    @staticmethod
    def apply(img: np.ndarray) -> np.ndarray:
        # Convert to grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
            
        # Threshold to get text blocks
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Get coordinates of all non-zero pixels
        coords = np.column_stack(np.where(thresh > 0))
        if len(coords) == 0:
            return img
            
        # Find minAreaRect to get the angle
        angle = cv2.minAreaRect(coords)[-1]
        
        # Adjust angle to be between -45 and 45 degrees
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
            
        # If angle is very small, skip rotation
        if abs(angle) < 0.5:
            return img
            
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        
        # Get rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
