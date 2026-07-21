import json
from loguru import logger
from app.modules.llm.service import LLMService
from app.modules.code_extraction.prompt import CodePrompt
from app.modules.code_extraction.schemas import CodeJSON
from app.modules.code_extraction.exceptions import CodeExtractionError

class CodeMerger:
    @staticmethod
    def merge(job_id: str, code_snippets: list) -> tuple[CodeJSON, int]:
        logger.info(f"Merging {len(code_snippets)} code snippets for job {job_id}")
        
        if not code_snippets:
            logger.warning(f"No code snippets to merge for {job_id}. Returning empty.")
            return CodeJSON(language="Unknown", confidence=1.0, description="No programming content found.", files=[]), 0
        
        system = CodePrompt.get_merge_system_prompt()
        user = CodePrompt.get_merge_user_prompt(code_snippets)
        
        try:
            content, tokens = LLMService.generate_single(system, user)
            
            # Clean possible markdown block
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
                
            data = json.loads(content)
            return CodeJSON(**data), tokens
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM final code JSON: {content}")
            raise CodeExtractionError(details={"reason": "Invalid JSON format from LLM merge", "raw": content})
        except Exception as e:
            logger.error(f"Merge failed: {str(e)}")
            raise CodeExtractionError(details={"error": str(e)})
