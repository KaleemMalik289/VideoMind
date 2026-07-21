import json
import shutil
from pathlib import Path
from loguru import logger
from app.modules.video.schemas import FrameMetadata

class FrameSelector:
    """Selects and moves unique frames into their final destination, correlating with scene metadata."""
    
    @staticmethod
    def process_unique_frames(
        job_id: str,
        unique_paths: list[str], 
        scenes: list[dict], 
        extracted_frames_info: list[dict], 
        output_dir: Path
    ) -> list[FrameMetadata]:
        
        logger.info(f"Generating unique frame collection for job {job_id}")
        
        final_frames = []
        
        for idx, path_str in enumerate(unique_paths):
            original_path = Path(path_str)
            if not original_path.exists():
                continue
                
            # Find original frame info
            frame_info = next((f for f in extracted_frames_info if f["path"] == path_str), None)
            if not frame_info:
                continue
                
            frame_num = frame_info["frame_number"]
            
            # Correlate with scene
            scene_id = None
            for scene in scenes:
                if scene["start_frame"] <= frame_num <= scene["end_frame"]:
                    scene_id = scene["scene_id"]
                    break
            
            # Copy to unique_frames directory
            # Keep original names but they are now in a new folder
            new_path = output_dir / original_path.name
            shutil.copy2(original_path, new_path)
            
            metadata = FrameMetadata(
                frame_id=idx + 1,
                scene_id=scene_id,
                timestamp=frame_info["timestamp"],
                frame_number=frame_num,
                path=str(new_path)
            )
            final_frames.append(metadata)
            
        # Save metadata JSON for the frames
        metadata_file = output_dir / "unique_frames_metadata.json"
        with open(metadata_file, "w") as f:
            json_data = [m.model_dump() for m in final_frames]
            json.dump(json_data, f, indent=2)
            
        logger.info(f"Saved {len(final_frames)} unique frames and metadata to {output_dir}")
        return final_frames
