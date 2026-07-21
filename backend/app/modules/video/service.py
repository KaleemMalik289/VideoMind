from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.video.metadata import MetadataExtractor
from app.modules.video.extractor import FrameExtractor
from app.modules.video.scene_detector import SceneDetectorWrapper
from app.modules.video.duplicate_detector import DuplicateDetector
from app.modules.video.frame_selector import FrameSelector
from app.modules.video.schemas import VideoProcessingResponse
from app.modules.video.exceptions import VideoProcessingError

class VideoProcessorService:
    """Orchestrates the entire video processing pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        """Ensures all necessary subdirectories exist for the video pipeline."""
        base_path = Path(settings.PROCESSED_DIR) / job_id
        dirs = {
            "metadata": base_path / "metadata",
            "frames": base_path / "frames",
            "unique_frames": base_path / "unique_frames",
            "logs": base_path / "logs"
        }
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    @staticmethod
    def process_video(job_id: str, video_path: str) -> VideoProcessingResponse:
        """Runs the complete video processing pipeline."""
        logger.info(f"Starting Video Processing Pipeline for job {job_id}")
        
        try:
            # 1. Ensure Directories
            dirs = VideoProcessorService.ensure_directories(job_id)
            
            # 2. Metadata Extraction
            video_metadata = MetadataExtractor.extract_metadata(
                job_id=job_id, 
                video_path=video_path, 
                output_dir=dirs["metadata"]
            )
            
            # 3. Frame Extraction
            extracted_frames = FrameExtractor.extract_frames(
                video_path=video_path, 
                output_dir=dirs["frames"], 
                fps=video_metadata.fps
            )
            
            # 4. Scene Detection
            scenes = SceneDetectorWrapper.detect_scenes(video_path=video_path)
            
            # 5. Duplicate Detection
            frame_paths = [f["path"] for f in extracted_frames]
            unique_paths = DuplicateDetector.filter_duplicates(frame_paths)
            
            # 6. Frame Selection & Metadata Saving
            final_frames = FrameSelector.process_unique_frames(
                job_id=job_id,
                unique_paths=unique_paths,
                scenes=scenes,
                extracted_frames_info=extracted_frames,
                output_dir=dirs["unique_frames"]
            )
            
            logger.info(f"Successfully completed Video Processing Pipeline for job {job_id}")
            
            return VideoProcessingResponse(
                success=True,
                job_id=job_id,
                message="Video processing completed successfully.",
                data={
                    "total_frames_extracted": len(extracted_frames),
                    "total_scenes_detected": len(scenes),
                    "unique_frames_saved": len(final_frames)
                }
            )
            
        except Exception as e:
            logger.error(f"Video Processing Pipeline failed for job {job_id}: {str(e)}")
            raise VideoProcessingError(details={"error": str(e)})
