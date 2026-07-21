import cv2
import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.video.reader import VideoReader

class FrameExtractor:
    """Extracts frames from video at configured intervals."""
    
    @staticmethod
    def extract_frames(video_path: str, output_dir: Path, fps: float) -> list:
        """Extracts frames at FRAME_EXTRACTION_RATE and resizes them."""
        logger.info(f"Starting interval frame extraction from {video_path}")
        
        extraction_rate = settings.FRAME_EXTRACTION_RATE
        interval_frames = int(fps / extraction_rate) if fps > extraction_rate else 1
        
        target_width = settings.OUTPUT_IMAGE_WIDTH
        target_height = settings.OUTPUT_IMAGE_HEIGHT
        img_format = settings.FRAME_IMAGE_FORMAT
        
        extracted_frames_info = []
        
        with VideoReader(video_path) as reader:
            total_frames = reader.get_properties()["total_frames"]
            
            for frame_number in range(0, total_frames, interval_frames):
                frame = reader.read_frame(frame_number)
                if frame is None:
                    continue
                    
                # Resize frame
                resized_frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
                
                # Format timestamp HH:MM:SS
                timestamp_sec = int(frame_number / fps)
                timestamp_str = time.strftime('%H:%M:%S', time.gmtime(timestamp_sec))
                
                # Save frame
                frame_filename = f"frame_{frame_number:06d}{img_format}"
                frame_path = output_dir / frame_filename
                cv2.imwrite(str(frame_path), resized_frame, [cv2.IMWRITE_JPEG_QUALITY, settings.FRAME_IMAGE_QUALITY])
                
                extracted_frames_info.append({
                    "frame_number": frame_number,
                    "timestamp": timestamp_str,
                    "path": str(frame_path)
                })
                
        logger.info(f"Extracted {len(extracted_frames_info)} interval frames.")
        return extracted_frames_info
