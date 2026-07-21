from app.core.exceptions import BaseAPIException

class NotesError(BaseAPIException):
    def __init__(self, message: str = "Notes generation failed.", details: dict = None):
        super().__init__(message=message, error_code="NOTES_ERROR", status_code=500, details=details)

class NotesValidationError(BaseAPIException):
    def __init__(self, message: str = "Notes validation failed.", details: dict = None):
        super().__init__(message=message, error_code="NOTES_VALIDATION_ERROR", status_code=400, details=details)
