import json
from loguru import logger
from app.modules.llm.service import LLMService
from app.modules.notes.prompt import NotesPrompt
from app.modules.notes.schemas import NotesJSON
from app.modules.notes.exceptions import NotesError

class NotesMerger:
    @staticmethod
    def merge(job_id: str, chunk_notes: list) -> tuple[NotesJSON, int]:
        logger.info(f"Merging {len(chunk_notes)} chunk notes for job {job_id}")
        
        system = NotesPrompt.get_merge_system_prompt()
        user = NotesPrompt.get_merge_user_prompt(chunk_notes)
        
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
            return NotesJSON(**data), tokens
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM final JSON: {content}")
            raise NotesError(details={"reason": "Invalid JSON format from LLM merge", "raw": content})
        except Exception as e:
            logger.error(f"Merge failed: {str(e)}")
            raise NotesError(details={"error": str(e)})
