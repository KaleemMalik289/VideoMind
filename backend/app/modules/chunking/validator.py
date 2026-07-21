import os
from loguru import logger
from app.modules.chunking.exceptions import ChunkingValidationError

class TimelineValidator:
    """Validates that a timeline JSON exists before chunking."""
    
    @staticmethod
    def validate(timeline_path: str) -> None:
        if not os.path.exists(timeline_path):
            logger.error(f"Missing timeline file: {timeline_path}")
            raise ChunkingValidationError(details={"path": timeline_path, "reason": "Timeline JSON is missing"})
