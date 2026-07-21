from app.core.exceptions import BaseAPIException

class VideoProcessingError(BaseAPIException):
    def __init__(self, message: str = "Video processing failed.", details: dict = None):
        super().__init__(message=message, error_code="VIDEO_PROCESSING_ERROR", status_code=500, details=details)

class CorruptedVideoError(BaseAPIException):
    def __init__(self, message: str = "The video file is corrupted or unreadable.", details: dict = None):
        super().__init__(message=message, error_code="CORRUPTED_VIDEO", status_code=400, details=details)

class UnsupportedCodecError(BaseAPIException):
    def __init__(self, message: str = "The video codec is unsupported.", details: dict = None):
        super().__init__(message=message, error_code="UNSUPPORTED_CODEC", status_code=400, details=details)
