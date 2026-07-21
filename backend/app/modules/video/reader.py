import cv2
from pathlib import Path
from loguru import logger
from app.modules.video.exceptions import CorruptedVideoError, UnsupportedCodecError

class VideoReader:
    """Wraps OpenCV VideoCapture to read frames securely."""
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            logger.error(f"Failed to open video: {video_path}")
            raise CorruptedVideoError()
            
    def get_properties(self) -> dict:
        """Extracts basic properties from the OpenCV capture object."""
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Approximate duration
        duration = total_frames / fps if fps > 0 else 0
        
        return {
            "fps": fps,
            "total_frames": total_frames,
            "width": width,
            "height": height,
            "duration": duration
        }
        
    def read_frame(self, frame_number: int):
        """Seeks to a frame and reads it."""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if not ret:
            logger.warning(f"Could not read frame {frame_number}")
            return None
        return frame
        
    def release(self):
        self.cap.release()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
