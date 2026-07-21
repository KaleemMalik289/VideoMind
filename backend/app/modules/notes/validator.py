import os
from loguru import logger
from app.modules.notes.exceptions import NotesValidationError

class NotesValidator:
    @staticmethod
    def validate(chunks_path: str) -> None:
        if not os.path.exists(chunks_path):
            logger.error(f"Missing chunks file: {chunks_path}")
            raise NotesValidationError(details={"path": chunks_path, "reason": "Semantic chunks missing"})
