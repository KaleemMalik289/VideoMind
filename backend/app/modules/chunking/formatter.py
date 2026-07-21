import json
from pathlib import Path
from app.modules.chunking.schemas import ChunkJSON

class ChunkFormatter:
    """Formats chunked results into JSON and Plain Text."""
    
    @staticmethod
    def save_json(result: ChunkJSON, output_path: Path) -> Path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.model_dump_json(indent=2))
        return output_path
        
    @staticmethod
    def save_text(result: ChunkJSON, output_path: Path) -> Path:
        with open(output_path, "w", encoding="utf-8") as f:
            for chunk in result.chunks:
                f.write(f"Chunk {chunk.chunk_id}\n\n")
                
                # Format time
                s_min, s_sec = divmod(int(chunk.start), 60)
                e_min, e_sec = divmod(int(chunk.end), 60)
                
                f.write(f"Time\n\n{s_min:02d}:{s_sec:02d} -> {e_min:02d}:{e_sec:02d}\n\n")
                
                if chunk.transcript:
                    f.write(f"Transcript\n\n{chunk.transcript}\n\n")
                    
                if chunk.ocr_text:
                    f.write(f"OCR\n\n")
                    for t in chunk.ocr_text:
                        f.write(f"{t}\n\n")
                        
                if chunk.frames:
                    frames_str = ",".join(map(str, chunk.frames))
                    f.write(f"Frames\n\n{frames_str}\n\n")
                    
                f.write("---\n\n")
                
        return output_path
