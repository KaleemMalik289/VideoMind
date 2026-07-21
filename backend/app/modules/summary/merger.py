import json
from loguru import logger
from app.modules.llm.service import LLMService
from app.modules.summary.prompt import SummaryPrompt
from app.modules.summary.schemas import SummaryJSON
from app.modules.summary.exceptions import SummaryError

class SummaryMerger:
    @staticmethod
    def merge(job_id: str, chunk_summaries: list) -> tuple[SummaryJSON, int]:
        logger.info(f"Merging {len(chunk_summaries)} chunk summaries for job {job_id}")
        
        system = SummaryPrompt.get_merge_system_prompt()
        user = SummaryPrompt.get_merge_user_prompt(chunk_summaries)
        
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
            return SummaryJSON(**data), tokens
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM final JSON: {content}")
            raise SummaryError(details={"reason": "Invalid JSON format from LLM merge", "raw": content})
        except Exception as e:
            logger.error(f"Merge failed: {str(e)}")
            raise SummaryError(details={"error": str(e)})
