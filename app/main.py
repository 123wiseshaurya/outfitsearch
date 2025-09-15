import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime

from app.api.endpoints import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Outfit Curation Engine API",
    description="An intelligent outfit recommendation system that curates outfits based on user preferences, inventory, and occasion.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix="/api/v1", tags=["outfits"])

# Mount static frontend at /ui (serve index.html when requesting /ui)
app.mount("/ui", StaticFiles(directory="app/static", html=True), name="ui")

@app.get("/")
@app.get("/health", tags=["health"])
async def root():
    logger.info("Root endpoint called")
    return {
        "status": "healthy",
        "message": "Welcome to the Outfit Curation Engine API",
        "docs": "/docs",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
