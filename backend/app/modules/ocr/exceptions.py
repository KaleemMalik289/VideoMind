from app.core.exceptions import BaseAPIException

class OCRError(BaseAPIException):
    def __init__(self, message: str = "OCR processing failed.", details: dict = None):
        super().__init__(message=message, error_code="OCR_PROCESSING_ERROR", status_code=500, details=details)

class OCRValidationError(BaseAPIException):
    def __init__(self, message: str = "OCR validation failed.", details: dict = None):
        super().__init__(message=message, error_code="OCR_VALIDATION_ERROR", status_code=400, details=details)
