from app.core.exceptions import BaseAPIException

class ChunkingError(BaseAPIException):
    def __init__(self, message: str = "Semantic chunking failed.", details: dict = None):
        super().__init__(message=message, error_code="CHUNKING_ERROR", status_code=500, details=details)

class ChunkingValidationError(BaseAPIException):
    def __init__(self, message: str = "Chunking validation failed.", details: dict = None):
        super().__init__(message=message, error_code="CHUNKING_VALIDATION_ERROR", status_code=400, details=details)
