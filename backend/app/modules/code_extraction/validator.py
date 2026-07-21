import os
from loguru import logger
from app.modules.code_extraction.exceptions import CodeValidationError

class CodeExtractionValidator:
    @staticmethod
    def validate(chunks_path: str) -> None:
        if not os.path.exists(chunks_path):
            logger.error(f"Missing chunks file: {chunks_path}")
            raise CodeValidationError(details={"path": chunks_path, "reason": "Semantic chunks missing"})
