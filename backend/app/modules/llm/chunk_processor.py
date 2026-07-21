import os
import json
from pathlib import Path
from loguru import logger
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from app.modules.llm.providers.base import BaseLLMProvider
from app.modules.llm.prompt_builder import PromptBuilder
from app.modules.llm.schemas import LLMChunkResponse
from app.modules.llm.exceptions import LLMError

class ChunkProcessor:
    """Processes semantic chunks individually with automatic retries and checkpointing."""
    
    def __init__(self, provider: BaseLLMProvider, raw_dir: Path):
        self.provider = provider
        self.raw_dir = raw_dir
        
    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(LLMError)
    )
    def _call_llm_with_retry(self, system_prompt: str, user_prompt: str) -> tuple[str, int]:
        return self.provider.generate(system_prompt, user_prompt)
        
    def process(self, chunk: dict, system_prompt: str, user_prompt_template: str) -> LLMChunkResponse:
        chunk_id = chunk["chunk_id"]
        output_file = self.raw_dir / f"chunk_{chunk_id:03d}.json"
        
        # Checkpoint resume
        if output_file.exists():
            with open(output_file, "r", encoding="utf-8") as f:
                logger.info(f"Skipping chunk {chunk_id}, already processed.")
                return LLMChunkResponse(**json.load(f))
                
        logger.info(f"Processing chunk {chunk_id} via {self.provider.__class__.__name__}")
        
        user_prompt = PromptBuilder.build_chunk_prompt(chunk, user_prompt_template)
        
        try:
            content, tokens = self._call_llm_with_retry(system_prompt, user_prompt)
        except Exception as e:
            logger.error(f"Failed to process chunk {chunk_id} after retries: {str(e)}")
            raise
            
        response = LLMChunkResponse(
            chunk_id=chunk_id,
            start=chunk["start"],
            end=chunk["end"],
            content=content,
            tokens_used=tokens,
            model=getattr(self.provider, "model", "unknown")
        )
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.model_dump_json(indent=2))
            
        return response
