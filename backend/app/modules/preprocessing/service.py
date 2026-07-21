import json
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.preprocessing.processor import ImageProcessor
from app.modules.preprocessing.schemas import PreprocessingResponse
from app.modules.preprocessing.exceptions import ImageProcessingError
from concurrent.futures import ProcessPoolExecutor, as_completed

class PreprocessingService:
    """Orchestrates the batch preprocessing of images for a job."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> Path:
        """Ensures the preprocessed_frames directory exists."""
        output_dir = Path(settings.PROCESSED_DIR) / job_id / "preprocessed_frames"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
        
    @staticmethod
    def process_job(job_id: str) -> PreprocessingResponse:
        """Processes all unique frames for a job in parallel."""
        logger.info(f"Starting Preprocessing Pipeline for job {job_id}")
        
        try:
            input_dir = Path(settings.PROCESSED_DIR) / job_id / "unique_frames"
            if not input_dir.exists():
                raise FileNotFoundError(f"No unique_frames directory found for job {job_id}")
                
            output_dir = PreprocessingService.ensure_directories(job_id)
            
            # We can read the unique_frames_metadata.json to get the exact list
            metadata_file = input_dir / "unique_frames_metadata.json"
            if not metadata_file.exists():
                raise FileNotFoundError(f"Missing unique_frames_metadata.json for job {job_id}")
                
            with open(metadata_file, "r") as f:
                unique_frames = json.load(f)
                
            if not unique_frames:
                logger.warning(f"No frames to process for job {job_id}")
                return PreprocessingResponse(
                    success=True,
                    job_id=job_id,
                    message="No frames to process.",
                    data={"processed_count": 0}
                )

            # Use ProcessPoolExecutor to bypass GIL and process frames in parallel across CPU cores
            # We map the process_frame function across the frame list.
            results = []
            
            # Since ImageProcessor has static methods, it can be pickled for multiprocessing
            with ProcessPoolExecutor() as executor:
                futures = {
                    executor.submit(
                        ImageProcessor.process_frame, 
                        frame["frame_id"], 
                        frame["path"], 
                        output_dir
                    ): frame for frame in unique_frames
                }
                
                for future in as_completed(futures):
                    result = future.result()
                    results.append(result.model_dump())
                    
            # Sort results by frame_id to keep them sequential
            results = sorted(results, key=lambda x: x["frame_id"])
            
            # Save the preprocessing metadata
            out_metadata_file = output_dir / "preprocessing_metadata.json"
            with open(out_metadata_file, "w") as f:
                json.dump(results, f, indent=2)
                
            logger.info(f"Successfully preprocessed {len(results)} frames for job {job_id}")
            
            return PreprocessingResponse(
                success=True,
                job_id=job_id,
                message="Image preprocessing completed successfully.",
                data={"processed_count": len(results)}
            )
            
        except Exception as e:
            logger.error(f"Preprocessing Pipeline failed for job {job_id}: {str(e)}")
            raise ImageProcessingError(details={"error": str(e)})
