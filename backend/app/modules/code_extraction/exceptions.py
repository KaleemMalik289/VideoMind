from app.core.exceptions import BaseAPIException

class CodeExtractionError(BaseAPIException):
    def __init__(self, message: str = "Code extraction failed.", details: dict = None):
        super().__init__(message=message, error_code="CODE_EXTRACTION_ERROR", status_code=500, details=details)

class CodeValidationError(BaseAPIException):
    def __init__(self, message: str = "Code validation failed.", details: dict = None):
        super().__init__(message=message, error_code="CODE_VALIDATION_ERROR", status_code=400, details=details)
