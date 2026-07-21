from app.core.exceptions import BaseAPIException

class AudioExtractionError(BaseAPIException):
    def __init__(self, message: str = "Audio extraction failed.", details: dict = None):
        super().__init__(message=message, error_code="AUDIO_EXTRACTION_ERROR", status_code=500, details=details)

class AudioValidationError(BaseAPIException):
    def __init__(self, message: str = "Audio validation failed.", details: dict = None):
        super().__init__(message=message, error_code="AUDIO_VALIDATION_ERROR", status_code=400, details=details)
