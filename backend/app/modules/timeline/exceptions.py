from app.core.exceptions import BaseAPIException

class TimelineError(BaseAPIException):
    def __init__(self, message: str = "Timeline generation failed.", details: dict = None):
        super().__init__(message=message, error_code="TIMELINE_GENERATION_ERROR", status_code=500, details=details)

class TimelineValidationError(BaseAPIException):
    def __init__(self, message: str = "Timeline validation failed.", details: dict = None):
        super().__init__(message=message, error_code="TIMELINE_VALIDATION_ERROR", status_code=400, details=details)
