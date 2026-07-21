import json
from pathlib import Path
from app.modules.transcription.schemas import TranscriptJSON

class TranscriptFormatter:
    """Formats transcript results into JSON and Plain Text."""
    
    @staticmethod
    def save_json(result: TranscriptJSON, output_path: Path) -> Path:
        """Saves the structured JSON representation."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.model_dump_json(indent=2))
            
        return output_path
        
    @staticmethod
    def save_text(result: TranscriptJSON, output_path: Path) -> Path:
        """Saves the human-readable chronologically formatted text representation."""
        with open(output_path, "w", encoding="utf-8") as f:
            for seg in result.segments:
                # Format: [00:00 - 00:06]
                start_min, start_sec = divmod(int(seg.start), 60)
                end_min, end_sec = divmod(int(seg.end), 60)
                
                time_block = f"[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}]"
                f.write(f"{time_block}\n\n{seg.text}\n\n")
                
        return output_path
