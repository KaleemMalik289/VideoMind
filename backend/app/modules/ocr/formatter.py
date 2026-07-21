import json
from pathlib import Path
from app.modules.ocr.schemas import OCRFrameResult

class OutputFormatter:
    """Formats OCR results into JSON and Plain Text."""
    
    @staticmethod
    def save_json(result: OCRFrameResult, output_dir: Path) -> Path:
        """Saves the structured JSON representation."""
        filename = f"frame_{result.frame_id:06d}.json"
        filepath = output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result.model_dump_json(indent=2))
            
        return filepath
        
    @staticmethod
    def save_text(result: OCRFrameResult, output_dir: Path) -> Path:
        """Saves the human-readable text representation."""
        filename = f"frame_{result.frame_id:06d}.txt"
        filepath = output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            for det in result.detections:
                f.write(f"{det.text}\n\n")
                
        return filepath
