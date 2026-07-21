import os
from loguru import logger
from app.modules.summary.exceptions import SummaryValidationError

class SummaryValidator:
    @staticmethod
    def validate(chunks_path: str) -> None:
        if not os.path.exists(chunks_path):
            logger.error(f"Missing chunks file: {chunks_path}")
            raise SummaryValidationError(details={"path": chunks_path, "reason": "Semantic chunks missing"})
