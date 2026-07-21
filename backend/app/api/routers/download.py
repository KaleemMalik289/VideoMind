import os
import shutil
import tempfile
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.settings import settings

router = APIRouter(tags=["AI Results"])

@router.get("/download/{job_id}")
async def download_results(job_id: str):
    job_dir = Path(settings.PROCESSED_DIR) / job_id
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found.")
        
    temp_dir = Path(tempfile.gettempdir()) / f"videomind_{job_id}"
    zip_path = Path(tempfile.gettempdir()) / f"videomind_{job_id}.zip"
    
    try:
        # We don't want to zip the original video or intermediate raw frames to save bandwidth
        # We'll just zip summary, notes, code, transcription, ocr, timeline, chunks
        
        target_dirs = ["summary", "notes", "code", "transcription", "ocr", "timeline", "chunks"]
        
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        has_data = False
        for d in target_dirs:
            src = job_dir / d
            dst = temp_dir / d
            if src.exists():
                shutil.copytree(src, dst)
                has_data = True
                
        if not has_data:
            raise HTTPException(status_code=404, detail="No generated artifacts found for this job.")
                
        shutil.make_archive(str(temp_dir), 'zip', str(temp_dir))
        
        return FileResponse(
            path=str(zip_path), 
            filename=f"videomind_results_{job_id}.zip", 
            media_type="application/zip"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate ZIP archive: {str(e)}")
