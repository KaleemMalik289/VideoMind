from pydantic import BaseModel
from typing import List

class OCRDetection(BaseModel):
    text: str
    confidence: float
    bounding_box: List[List[float]] # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

class OCRFrameResult(BaseModel):
    frame_id: int
    timestamp: str
    image: str
    detections: List[OCRDetection]

class OCRResponse(BaseModel):
    success: bool
    job_id: str
    message: str
    data: dict
