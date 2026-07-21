from fastapi import FastAPI
from app.core.settings import settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from loguru import logger

# Initialize logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Exception Handlers
setup_exception_handlers(app)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up VideoMind AI Backend MVP")

@app.get("/health")
def health_check():
    return {"success": True, "message": "Backend is running"}

from app.api.router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

