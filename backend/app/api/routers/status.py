from fastapi import APIRouter
from app.schemas.response import APIResponse

router = APIRouter(tags=["Status"])

@router.get("/status/{job_id}", response_model=APIResponse)
async def get_status(job_id: str):
    """Retrieves the processing status of a job."""
    from pathlib import Path
    from app.core.settings import settings
    
    base_dir = Path(settings.PROCESSED_DIR) / job_id
    if not base_dir.exists():
        return APIResponse(success=False, message="Job not found.", data={"status": "not_found"})
        
    # Check progressive directories
    if (base_dir / "code" / "code.json").exists():
        status = "completed"
    elif (base_dir / "notes" / "notes.json").exists():
        status = "generating_code"
    elif (base_dir / "summary" / "summary.json").exists():
        status = "generating_notes"
    elif (base_dir / "llm" / "merged" / "merged_response.json").exists():
        status = "generating_summary"
    elif (base_dir / "chunks" / "chunks.json").exists():
        status = "llm_orchestration"
    elif (base_dir / "timeline" / "timeline.json").exists():
        status = "semantic_chunking"
    elif (base_dir / "transcription" / "transcript.json").exists():
        status = "timeline_building"
    elif (base_dir / "ocr" / "json").exists() and list((base_dir / "ocr" / "json").glob("*.json")):
        status = "transcription"
    elif (base_dir / "preprocessed_frames").exists() and list((base_dir / "preprocessed_frames").glob("*.jpg")):
        status = "ocr"
    elif (base_dir / "unique_frames" / "unique_frames_metadata.json").exists():
        status = "preprocessing"
    elif (base_dir / "frames").exists() and list((base_dir / "frames").glob("*.jpg")):
        status = "extracting_unique_frames"
    elif (base_dir / "original").exists():
        status = "extracting_frames"
    else:
        status = "queued"
        
    return APIResponse(
        success=True,
        message="Status retrieved.",
        data={"job_id": job_id, "status": status}
    )
