from app.core.exceptions import BaseAPIException

class SummaryError(BaseAPIException):
    def __init__(self, message: str = "Summary generation failed.", details: dict = None):
        super().__init__(message=message, error_code="SUMMARY_ERROR", status_code=500, details=details)

class SummaryValidationError(BaseAPIException):
    def __init__(self, message: str = "Summary validation failed.", details: dict = None):
        super().__init__(message=message, error_code="SUMMARY_VALIDATION_ERROR", status_code=400, details=details)
