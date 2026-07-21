from typing import Any, Dict, Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class APIErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    details: Optional[Dict[str, Any]] = None
