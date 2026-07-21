from app.core.exceptions import BaseAPIException

class TranscriptionError(BaseAPIException):
    def __init__(self, message: str = "Transcription failed.", details: dict = None):
        super().__init__(message=message, error_code="TRANSCRIPTION_ERROR", status_code=500, details=details)

class TranscriptionValidationError(BaseAPIException):
    def __init__(self, message: str = "Transcription validation failed.", details: dict = None):
        super().__init__(message=message, error_code="TRANSCRIPTION_VALIDATION_ERROR", status_code=400, details=details)
