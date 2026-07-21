import json

class PromptBuilder:
    """Builds consistent dynamic prompts mapping semantic chunks to the desired LLM task."""
    
    @staticmethod
    def build_chunk_prompt(chunk: dict, user_prompt: str) -> str:
        """
        Wraps a specific chunk's data into a consistent block and appends the user's prompt.
        """
        s_min, s_sec = divmod(int(chunk.get("start", 0)), 60)
        e_min, e_sec = divmod(int(chunk.get("end", 0)), 60)
        
        time_str = f"{s_min:02d}:{s_sec:02d} -> {e_min:02d}:{e_sec:02d}"
        
        prompt = f"""--- CHUNK CONTEXT ---
Time Range: {time_str}

[TRANSCRIPT]
{chunk.get('transcript', 'No transcript available.')}

[OCR TEXT]
{chr(10).join(chunk.get('ocr_text', [])) if chunk.get('ocr_text') else 'No OCR text available.'}

--- END CHUNK CONTEXT ---

{user_prompt}
"""
        return prompt
