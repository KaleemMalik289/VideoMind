from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "VideoMind AI Backend"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Storage paths
    STORAGE_DIR: str = "storage"
    UPLOADS_DIR: str = f"{STORAGE_DIR}/uploads"
    PROCESSED_DIR: str = f"{STORAGE_DIR}/processed"
    OUTPUTS_DIR: str = f"{STORAGE_DIR}/outputs"
    TEMP_DIR: str = f"{STORAGE_DIR}/temp"
    MODELS_DIR: str = f"{STORAGE_DIR}/models"

    # Security
    SECRET_KEY: str = "supersecretkey-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis/Celery
    REDIS_URL: str = "redis://localhost:6379/0"

    # Upload Settings
    MAX_UPLOAD_SIZE: int = 2 * 1024 * 1024 * 1024  # 2GB
    ALLOWED_VIDEO_EXTENSIONS: list[str] = [".mp4", ".mov", ".avi", ".mkv", ".webm"]
    ALLOWED_MIME_TYPES: list[str] = [
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-matroska",
        "video/webm",
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
