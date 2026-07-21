from app.modules.ocr.schemas import OCRDetection
from app.core.settings import settings
from loguru import logger

class TextRecognizer:
    """Parses raw PaddleOCR outputs into structured detection schemas."""
    
    @staticmethod
    def parse_results(raw_results: list) -> list[OCRDetection]:
        """Extracts text, confidence, and bounding boxes, filtering by threshold."""
        detections = []
        threshold = settings.OCR_CONFIDENCE_THRESHOLD
        
        for line in raw_results:
            try:
                box = line[0]
                text_tuple = line[1]
                text = text_tuple[0]
                confidence = float(text_tuple[1])
                
                if confidence >= threshold:
                    detections.append(OCRDetection(
                        text=text,
                        confidence=confidence,
                        bounding_box=box
                    ))
            except Exception as e:
                logger.warning(f"Failed to parse a raw OCR line: {str(e)}")
                continue
                
        return detections
