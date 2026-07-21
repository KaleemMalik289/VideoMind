import os
import json
from pathlib import Path
from loguru import logger
from app.modules.video.schemas import VideoMetadata
from app.modules.video.reader import VideoReader

class MetadataExtractor:
    """Extracts and saves metadata from a video file."""
    
    @staticmethod
    def extract_metadata(job_id: str, video_path: str, output_dir: Path) -> VideoMetadata:
        """Extracts complete metadata and saves it to JSON."""
        logger.info(f"Extracting metadata for job {job_id}")
        
        file_size = os.path.getsize(video_path)
        filename = os.path.basename(video_path)
        
        with VideoReader(video_path) as reader:
            props = reader.get_properties()
            
        metadata = VideoMetadata(
            job_id=job_id,
            filename=filename,
            fps=props["fps"],
            duration=props["duration"],
            total_frames=props["total_frames"],
            width=props["width"],
            height=props["height"],
            file_size=file_size,
        )
        
        # Save to JSON
        metadata_file = output_dir / "video_metadata.json"
        with open(metadata_file, "w") as f:
            f.write(metadata.model_dump_json(indent=2))
            
        logger.info(f"Saved metadata for job {job_id} to {metadata_file}")
        return metadata
