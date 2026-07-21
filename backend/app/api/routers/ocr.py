import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.schemas.response import APIResponse
from app.core.settings import settings

router = APIRouter(tags=["AI Results"])

@router.get("/ocr/{job_id}", response_model=APIResponse)
async def get_ocr(job_id: str):
    json_dir = Path(settings.PROCESSED_DIR) / job_id / "ocr" / "json"
    if not json_dir.exists():
        raise HTTPException(status_code=404, detail="OCR results not found or not yet generated.")
        
    all_results = []
    for f_path in sorted(json_dir.glob("*.json")):
        with open(f_path, "r", encoding="utf-8") as f:
            all_results.append(json.load(f))
            
    return APIResponse(success=True, message="OCR results retrieved successfully.", data={"ocr": all_results})
