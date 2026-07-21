from app.core.settings import settings

class SummaryPrompt:
    
    @staticmethod
    def get_chunk_system_prompt() -> str:
        return f"""You are an expert content summarizer.
Your task is to summarize the provided chunk of a video (containing transcript and OCR text).
Write a very brief, dense summary of the key concepts discussed in this chunk.
Do not hallucinate. Do not introduce ideas not present in the text.
Write in a {settings.SUMMARY_STYLE} tone. Language: {settings.SUMMARY_LANGUAGE}.
"""

    @staticmethod
    def get_chunk_user_prompt() -> str:
        return """Please summarize the chunk provided above. Focus on main topics, facts, and transitions."""
        
    @staticmethod
    def get_merge_system_prompt() -> str:
        return f"""You are an expert content synthesizer.
You will be given a chronologically ordered list of summaries from various chunks of a video.
Your task is to synthesize these into a final, unified JSON document.

You MUST return ONLY valid JSON matching this schema:
{{
    "executive_summary": "1-2 paragraphs giving a high-level overview of the entire video.",
    "detailed_summary": "A comprehensive summary including major topics, explanations, and chronological flow. Remove duplicate ideas.",
    "bullet_summary": [
        "Key takeaway 1",
        "Key takeaway 2",
        "Important fact 3"
    ]
}}

Write in a {settings.SUMMARY_STYLE} tone. Language: {settings.SUMMARY_LANGUAGE}.
DO NOT wrap the response in markdown ```json blocks. Return raw JSON.
"""

    @staticmethod
    def get_merge_user_prompt(chunk_summaries: list) -> str:
        text = "Here are the chronological chunk summaries:\n\n"
        for i, s in enumerate(chunk_summaries, 1):
            text += f"--- Chunk {i} ---\n{s}\n\n"
            
        text += "Please synthesize these into the requested JSON schema."
        return text
