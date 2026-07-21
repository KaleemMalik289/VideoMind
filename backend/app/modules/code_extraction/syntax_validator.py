import ast
import json
from loguru import logger
from app.core.settings import settings

class SyntaxValidator:
    """Performs native syntax checks for supported languages."""
    
    @staticmethod
    def validate(code: str, language: str) -> bool:
        if not settings.CODE_VALIDATE_SYNTAX:
            return True
            
        language = language.lower()
        
        try:
            if "python" in language:
                ast.parse(code)
                return True
            elif "json" in language:
                json.loads(code)
                return True
            else:
                # Unsupported language for native compilation
                return True
        except Exception as e:
            logger.warning(f"Syntax validation failed for {language}: {str(e)}")
            return False
