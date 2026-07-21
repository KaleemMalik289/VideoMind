from app.core.exceptions import BaseAPIException

class InvalidYouTubeURLError(BaseAPIException):
    def __init__(self, message: str = "Invalid YouTube URL provided.", details: dict = None):
        super().__init__(message=message, error_code="INVALID_YOUTUBE_URL", status_code=400, details=details)

class DownloadFailedError(BaseAPIException):
    def __init__(self, message: str = "Failed to download the video from YouTube.", details: dict = None):
        super().__init__(message=message, error_code="DOWNLOAD_FAILED", status_code=500, details=details)
