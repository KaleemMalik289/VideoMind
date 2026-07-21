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

    # Video Processing Settings
    FRAME_EXTRACTION_RATE: int = 1
    FRAME_IMAGE_FORMAT: str = ".jpg"
    FRAME_IMAGE_QUALITY: int = 95
    FRAME_SIMILARITY_THRESHOLD: float = 0.95
    SCENE_DETECTION_THRESHOLD: float = 27.0
    OUTPUT_IMAGE_WIDTH: int = 1280
    OUTPUT_IMAGE_HEIGHT: int = 720

    # Preprocessing Settings
    PREPROCESS_ENABLE_RESIZE: bool = True
    PREPROCESS_ENABLE_DENOISE: bool = True
    PREPROCESS_ENABLE_SHARPEN: bool = True
    PREPROCESS_ENABLE_CONTRAST: bool = True
    PREPROCESS_ENABLE_THRESHOLD: bool = False
    PREPROCESS_ENABLE_ROTATION: bool = False
    
    PREPROCESS_IMAGE_WIDTH: int = 1920
    PREPROCESS_IMAGE_HEIGHT: int = 1080
    PREPROCESS_CLAHE_CLIP_LIMIT: float = 2.0
    PREPROCESS_OUTPUT_QUALITY: int = 95

    # OCR Settings
    OCR_LANGUAGE: str = "en"
    OCR_USE_GPU: bool = True
    OCR_BATCH_SIZE: int = 8
    OCR_CONFIDENCE_THRESHOLD: float = 0.30
    OCR_ENABLE_ANGLE_CLASSIFIER: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
