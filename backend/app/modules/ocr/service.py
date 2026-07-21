import json
import os
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.ocr.validator import ImageValidator
from app.modules.ocr.detector import TextDetector
from app.modules.ocr.recognizer import TextRecognizer
from app.modules.ocr.cleaner import OCRCleaner
from app.modules.ocr.parser import OutputParser
from app.modules.ocr.formatter import OutputFormatter
from app.modules.ocr.schemas import OCRFrameResult, OCRResponse
from app.modules.ocr.exceptions import OCRError

class OCRService:
    """Orchestrates the OCR processing pipeline for all preprocessed frames in a job."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        """Ensures the JSON and Text output directories exist."""
        base_path = Path(settings.PROCESSED_DIR) / job_id / "ocr"
        dirs = {
            "json": base_path / "json",
            "text": base_path / "text",
            "logs": base_path / "logs" # keeping consistent
        }
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    @staticmethod
    def process_frame(frame_id: int, timestamp: str, original_filename: str, image_path: str, dirs: dict):
        """Runs a single frame through the OCR pipeline."""
        try:
            # 1. Validate
            ImageValidator.validate(image_path)
            
            # 2. Detect & Recognize
            raw_results = TextDetector.run_ocr(image_path)
            detections = TextRecognizer.parse_results(raw_results)
            
            # 3. Clean Text
            for det in detections:
                det.text = OCRCleaner.clean_text(det.text)
                
            # Filter out ones that became empty after cleaning
            detections = [d for d in detections if d.text]
            
            # 4. Sort Reading Order
            sorted_detections = OutputParser.sort_reading_order(detections)
            
            # 5. Format & Save
            result = OCRFrameResult(
                frame_id=frame_id,
                timestamp=timestamp,
                image=original_filename,
                detections=sorted_detections
            )
            
            OutputFormatter.save_json(result, dirs["json"])
            OutputFormatter.save_text(result, dirs["text"])
            
            logger.info(f"Successfully processed OCR for frame {frame_id}")
            return result
            
        except Exception as e:
            logger.error(f"OCR Pipeline failed for frame {frame_id}: {str(e)}")
            raise e

    @staticmethod
    def process_job(job_id: str) -> OCRResponse:
        """Processes all preprocessed frames for a job sequentially to prevent OOM."""
        logger.info(f"Starting OCR Pipeline for job {job_id}")
        
        try:
            dirs = OCRService.ensure_directories(job_id)
            
            # Read unique_frames_metadata.json to get timestamps
            job_base = Path(settings.PROCESSED_DIR) / job_id
            metadata_file = job_base / "unique_frames" / "unique_frames_metadata.json"
            
            if not metadata_file.exists():
                raise FileNotFoundError(f"Missing unique_frames_metadata.json for job {job_id}")
                
            with open(metadata_file, "r") as f:
                unique_frames = json.load(f)
                
            preprocessed_dir = job_base / "preprocessed_frames"
            
            processed_count = 0
            
            if settings.ENABLE_PARALLEL_OCR:
                logger.info(f"Using Parallel OCR (Batch Size: {settings.OCR_BATCH_SIZE})")
                from concurrent.futures import ThreadPoolExecutor, as_completed
                
                # We can't batch PaddleOCR directly easily without list of imgs, but we can thread it.
                # However, PaddleOCR might be thread-safe enough for this if CPU bound.
                def process_single(frame):
                    frame_id = frame["frame_id"]
                    timestamp = frame["timestamp"]
                    original_filename = os.path.basename(frame["path"])
                    preprocessed_path = preprocessed_dir / original_filename
                    
                    if preprocessed_path.exists():
                        OCRService.process_frame(
                            frame_id=frame_id,
                            timestamp=timestamp,
                            original_filename=original_filename,
                            image_path=str(preprocessed_path),
                            dirs=dirs
                        )
                        return 1
                    else:
                        logger.warning(f"Preprocessed frame missing: {preprocessed_path}")
                        return 0

                with ThreadPoolExecutor(max_workers=settings.MAX_CONCURRENT_JOBS) as executor:
                    futures = [executor.submit(process_single, frame) for frame in unique_frames]
                    for future in as_completed(futures):
                        processed_count += future.result()
            else:
                for frame in unique_frames:
                    frame_id = frame["frame_id"]
                    timestamp = frame["timestamp"]
                    original_filename = os.path.basename(frame["path"])
                    
                    preprocessed_path = preprocessed_dir / original_filename
                    
                    if preprocessed_path.exists():
                        OCRService.process_frame(
                            frame_id=frame_id,
                            timestamp=timestamp,
                            original_filename=original_filename,
                            image_path=str(preprocessed_path),
                            dirs=dirs
                        )
                        processed_count += 1
                    else:
                        logger.warning(f"Preprocessed frame missing: {preprocessed_path}")
                    
            logger.info(f"Successfully completed OCR Pipeline for job {job_id}. Processed {processed_count} frames.")
            
            return OCRResponse(
                success=True,
                job_id=job_id,
                message="OCR pipeline completed successfully.",
                data={"processed_frames": processed_count}
            )
            
        except Exception as e:
            logger.error(f"OCR Pipeline failed for job {job_id}: {str(e)}")
            raise OCRError(details={"error": str(e)})
