from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from loguru import logger

class BaseAPIException(Exception):
    def __init__(self, message: str, error_code: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAPIException)
    async def custom_exception_handler(request: Request, exc: BaseAPIException):
        logger.error(f"API Error: {exc.error_code} - {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "error_code": exc.error_code,
                "details": exc.details
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled Exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
                "error_code": "INTERNAL_ERROR",
                "details": {}
            }
        )
