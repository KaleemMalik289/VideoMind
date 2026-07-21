from scenedetect import detect, ContentDetector
from loguru import logger
from app.core.settings import settings

class SceneDetectorWrapper:
    """Wraps PySceneDetect to find scene boundaries."""
    
    @staticmethod
    def detect_scenes(video_path: str) -> list:
        """Runs content-aware scene detection on the video."""
        logger.info(f"Starting scene detection for {video_path}")
        
        threshold = settings.SCENE_DETECTION_THRESHOLD
        
        # detect returns a list of tuples (start_time, end_time)
        # where time is a FrameTimecode object
        try:
            scene_list = detect(video_path, ContentDetector(threshold=threshold))
            scenes = []
            for i, scene in enumerate(scene_list):
                scenes.append({
                    "scene_id": i + 1,
                    "start_frame": scene[0].get_frames(),
                    "end_frame": scene[1].get_frames(),
                    "start_timecode": scene[0].get_timecode(),
                    "end_timecode": scene[1].get_timecode()
                })
            logger.info(f"Detected {len(scenes)} scenes.")
            return scenes
        except Exception as e:
            logger.error(f"Scene detection failed: {str(e)}")
            return []
