from app.core.exceptions import BaseAPIException

class LLMError(BaseAPIException):
    def __init__(self, message: str = "LLM API request failed.", details: dict = None):
        super().__init__(message=message, error_code="LLM_ERROR", status_code=502, details=details)

class LLMValidationError(BaseAPIException):
    def __init__(self, message: str = "LLM validation failed.", details: dict = None):
        super().__init__(message=message, error_code="LLM_VALIDATION_ERROR", status_code=400, details=details)
