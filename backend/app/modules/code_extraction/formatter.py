import os
import json
from pathlib import Path
from app.modules.code_extraction.schemas import CodeJSON

class CodeFormatter:
    """Formats JSON into Markdown and raw source files."""
    
    @staticmethod
    def format(code_data: CodeJSON, dirs: dict) -> None:
        # 1. Save JSON
        with open(dirs["json"], "w", encoding="utf-8") as f:
            f.write(code_data.model_dump_json(indent=2))
            
        # 2. Save Markdown
        with open(dirs["markdown"], "w", encoding="utf-8") as f:
            f.write(f"# Reconstructed Code\n\n")
            f.write(f"**Language:** {code_data.language}\n")
            f.write(f"**Confidence:** {code_data.confidence * 100:.1f}%\n")
            f.write(f"**Description:** {code_data.description}\n\n")
            
            for file in code_data.files:
                f.write(f"## {file.filename}\n")
                f.write(f"*Timeline: {file.timeline}*\n\n")
                
                lang_tag = code_data.language.lower()
                f.write(f"```{lang_tag}\n")
                f.write(f"{file.code}\n")
                f.write(f"```\n\n")
                
        # 3. Save raw source files
        for file in code_data.files:
            source_path = dirs["source"] / file.filename
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(file.code)
