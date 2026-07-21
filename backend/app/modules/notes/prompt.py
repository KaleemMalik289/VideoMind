from app.core.settings import settings

class NotesPrompt:
    
    @staticmethod
    def get_chunk_system_prompt() -> str:
        return f"""You are an expert technical note-taker.
Your task is to extract highly granular, educational notes from the provided video chunk.
Extract ALL important facts, definitions, formulas, and examples.
Do not hallucinate. Do not write filler. Keep it extremely dense and concise.
Write in a {settings.NOTES_STYLE} style. Language: {settings.NOTES_LANGUAGE}.
"""

    @staticmethod
    def get_chunk_user_prompt() -> str:
        return """Please extract the raw educational notes from this chunk. Focus on technical accuracy, definitions, and examples."""
        
    @staticmethod
    def get_merge_system_prompt() -> str:
        return f"""You are an expert technical writer and educator.
You will be given a chronologically ordered list of granular notes extracted from a video.
Your task is to synthesize these into a final, exhaustive, beautifully structured JSON document.
Remove duplicated facts across chunks, but DO NOT drop any unique technical details, definitions, or examples.

You MUST return ONLY valid JSON matching this exact schema:
{{
    "title": "A concise, descriptive title for the entire video.",
    "introduction": "1-2 paragraphs introducing the core subject matter.",
    "sections": [
        {{
            "title": "Section Heading",
            "content": ["Bullet point 1", "Bullet point 2"],
            "definitions": ["Term: Definition"],
            "examples": ["Example explanation"],
            "formulas": ["Important formula or code snippet"]
        }}
    ],
    "conclusions": [
        "Final thought or conclusion 1"
    ]
}}

Write in a {settings.NOTES_STYLE} tone. Language: {settings.NOTES_LANGUAGE}.
DO NOT wrap the response in markdown ```json blocks. Return raw JSON.
"""

    @staticmethod
    def get_merge_user_prompt(chunk_notes: list) -> str:
        text = "Here are the chronological granular notes:\n\n"
        for i, n in enumerate(chunk_notes, 1):
            text += f"--- Chunk {i} ---\n{n}\n\n"
            
        text += "Please synthesize these into the requested JSON schema, maintaining all technical depth."
        return text
