from app.core.exceptions import BaseAPIException

class ImageProcessingError(BaseAPIException):
    def __init__(self, message: str = "Image preprocessing failed.", details: dict = None):
        super().__init__(message=message, error_code="IMAGE_PROCESSING_ERROR", status_code=500, details=details)

class ImageValidationError(BaseAPIException):
    def __init__(self, message: str = "Image validation failed.", details: dict = None):
        super().__init__(message=message, error_code="IMAGE_VALIDATION_ERROR", status_code=400, details=details)
