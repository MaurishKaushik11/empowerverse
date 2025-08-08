from fastapi import FastAPI, HTTPException, Depends, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
import uvicorn
import logging
from contextlib import asynccontextmanager

from app.database.database import engine, get_db, init_db
from app.database import models
from app.routers import recommendations, data_collection
from app.core.config import settings
from app.services.recommendation_engine import RecommendationEngine
from app.services.data_collector import DataCollector

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    # Continue anyway for development

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Video Recommendation Engine...")
    
    # Initialize recommendation engine
    recommendation_engine = RecommendationEngine()
    app.state.recommendation_engine = recommendation_engine
    
    # Initialize data collector
    data_collector = DataCollector()
    app.state.data_collector = data_collector
    
    yield
    
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Video Recommendation Engine",
    description="A sophisticated recommendation system for personalized video content",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])
app.include_router(data_collection.router, prefix="/api/v1", tags=["data-collection"])

@app.get("/")
async def root():
    return {
        "message": "Video Recommendation Engine API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "video-recommendation-engine"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )