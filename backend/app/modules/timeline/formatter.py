import json
from pathlib import Path
from app.modules.timeline.schemas import TimelineJSON

class TimelineFormatter:
    """Generates final JSON and plain text timeline representations."""
    
    @staticmethod
    def save_json(result: TimelineJSON, output_path: Path) -> Path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.model_dump_json(indent=2))
        return output_path
        
    @staticmethod
    def save_text(result: TimelineJSON, output_path: Path) -> Path:
        with open(output_path, "w", encoding="utf-8") as f:
            for entry in result.entries:
                start_min, start_sec = divmod(int(entry.start), 60)
                start_hour, start_min = divmod(start_min, 60)
                
                time_block = f"[{start_hour:02d}:{start_min:02d}:{start_sec:02d}]"
                f.write(f"{time_block}\n\n")
                
                if entry.transcript:
                    f.write(f"Transcript\n\n{entry.transcript}\n\n")
                    
                if entry.ocr_text:
                    f.write(f"OCR\n\n")
                    for t in entry.ocr_text:
                        f.write(f"{t}\n\n")
                        
                f.write("---\n\n")
                
        return output_path
