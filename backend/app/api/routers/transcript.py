import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.schemas.response import APIResponse
from app.core.settings import settings

router = APIRouter(tags=["AI Results"])

@router.get("/transcript/{job_id}", response_model=APIResponse)
async def get_transcript(job_id: str):
    file_path = Path(settings.PROCESSED_DIR) / job_id / "transcription" / "transcript.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Transcript not found or not yet generated.")
        
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    return APIResponse(success=True, message="Transcript retrieved successfully.", data={"transcript": data.get("segments", [])})
