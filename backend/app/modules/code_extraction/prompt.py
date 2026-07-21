from app.core.settings import settings

class CodePrompt:
    
    @staticmethod
    def get_chunk_system_prompt() -> str:
        return """You are an expert programming reconstructor.
Your task is to analyze the provided video chunk containing OCR text and transcripts.
Identify if there is any programming code, scripts, configuration files, or shell commands visible or discussed.
Extract the code EXACTLY. Do not fix logic errors, but fix OCR typos based on context.
If the chunk contains NO code, return exactly the string "NO_CODE_FOUND".
Otherwise, return the raw code blocks. Do not wrap in markdown or json. Just return the code context.
"""

    @staticmethod
    def get_chunk_user_prompt() -> str:
        return """Please extract the raw programming code from this chunk. If none exists, output NO_CODE_FOUND."""
        
    @staticmethod
    def get_merge_system_prompt() -> str:
        return """You are an expert software engineer.
You will be given a chronological sequence of code snippets extracted from a video tutorial.
Your task is to reconstruct the FINAL state of all files written in the video.
Merge the fragmented snippets into cohesive, complete files. Preserve indentation and syntax.
Identify the primary programming language.

You MUST return ONLY valid JSON matching this exact schema:
{
    "language": "Python",
    "confidence": 0.95,
    "description": "Brief description of what the code does",
    "files": [
        {
            "filename": "app.py",
            "timeline": "00:01:00 - 00:05:00",
            "code": "print('Hello World')"
        }
    ]
}
DO NOT wrap the response in markdown ```json blocks. Return raw JSON.
If there was absolutely no code in the entire video, return empty files array.
"""

    @staticmethod
    def get_merge_user_prompt(chunk_codes: list) -> str:
        text = "Here are the chronological code snippets:\n\n"
        for i, c in enumerate(chunk_codes, 1):
            if c.strip() and c.strip() != "NO_CODE_FOUND":
                text += f"--- Snippet {i} ---\n{c}\n\n"
                
        text += "Please reconstruct the final source code files into the requested JSON schema."
        return text
