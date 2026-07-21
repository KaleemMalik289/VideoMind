from app.core.exceptions import BaseAPIException

class UnsupportedFileTypeError(BaseAPIException):
    def __init__(self, message: str = "Unsupported file type.", details: dict = None):
        super().__init__(message=message, error_code="UNSUPPORTED_FILE_TYPE", status_code=400, details=details)

class FileSizeExceededError(BaseAPIException):
    def __init__(self, message: str = "File size exceeded the maximum limit.", details: dict = None):
        super().__init__(message=message, error_code="FILE_SIZE_EXCEEDED", status_code=413, details=details)

class EmptyFileError(BaseAPIException):
    def __init__(self, message: str = "The uploaded file is empty.", details: dict = None):
        super().__init__(message=message, error_code="EMPTY_FILE", status_code=400, details=details)

class FilenameSanitizationError(BaseAPIException):
    def __init__(self, message: str = "Invalid filename detected.", details: dict = None):
        super().__init__(message=message, error_code="INVALID_FILENAME", status_code=400, details=details)

class StorageError(BaseAPIException):
    def __init__(self, message: str = "Failed to save the file.", details: dict = None):
        super().__init__(message=message, error_code="STORAGE_ERROR", status_code=500, details=details)
