from fastapi import APIRouter, Depends, HTTPException, Header, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.database.database import get_db
from app.services.data_collector import DataCollector
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

def verify_flic_token(flic_token: str = Header(...)):
    """Verify the Flic-Token header for internal API access."""
    if flic_token != settings.FLIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Flic-Token")
    return flic_token

@router.post("/collect/viewed-posts")
async def collect_viewed_posts(
    background_tasks: BackgroundTasks,
    page: int = 1,
    page_size: int = 1000,
    flic_token: str = Depends(verify_flic_token),
    db: Session = Depends(get_db)
):
    """
    Collect all viewed posts data from the external API.
    This is an internal endpoint for data collection.
    """
    try:
        data_collector = DataCollector()
        
        # Run data collection in background
        background_tasks.add_task(
            data_collector.collect_viewed_posts,
            page=page,
            page_size=page_size,
            db=db
        )
        
        return {
            "status": "success",
            "message": "Viewed posts collection started",
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        logger.error(f"Error starting viewed posts collection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/collect/liked-posts")
async def collect_liked_posts(
    background_tasks: BackgroundTasks,
    page: int = 1,
    page_size: int = 1000,
    flic_token: str = Depends(verify_flic_token),
    db: Session = Depends(get_db)
):
    """
    Collect all liked posts data from the external API.
    """
    try:
        data_collector = DataCollector()
        
        background_tasks.add_task(
            data_collector.collect_liked_posts,
            page=page,
            page_size=page_size,
            db=db
        )
        
        return {
            "status": "success",
            "message": "Liked posts collection started",
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        logger.error(f"Error starting liked posts collection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/collect/inspired-posts")
async def collect_inspired_posts(
    background_tasks: BackgroundTasks,
    page: int = 1,
    page_size: int = 1000,
    flic_token: str = Depends(verify_flic_token),
    db: Session = Depends(get_db)
):
    """
    Collect all inspired posts data from the external API.
    """
    try:
        data_collector = DataCollector()
        
        background_tasks.add_task(
            data_collector.collect_inspired_posts,
            page=page,
            page_size=page_size,
            db=db
        )
        
        return {
            "status": "success",
            "message": "Inspired posts collection started",
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        logger.error(f"Error starting inspired posts collection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/collect/rated-posts")
async def collect_rated_posts(
    background_tasks: BackgroundTasks,
    page: int = 1,
    page_size: int = 1000,
    flic_token: str = Depends(verify_flic_token),
    db: Session = Depends(get_db)
):
    """
    Collect all rated posts data from the external API.
    """
    try:
        data_collector = DataCollector()
        
        background_tasks.add_task(
            data_collector.collect_rated_posts,
            page=page,
            page_size=page_size,
            db=db
        )
        
        return {
            "status": "success",
            "message": "Rated posts collection started",
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        logger.error(f"Error starting rated posts collection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/collect/all-posts")
async def collect_all_posts(
    background_tasks: BackgroundTasks,
    page: int = 1,
    page_size: int = 1000,
    flic_token: str = Depends(verify_flic_token),
    db: Session = Depends(get_db)
):
    """
    Collect all posts data from the external API.
    """
    try:
        data_collector = DataCollector()
        
        background_tasks.add_task(
            data_collector.collect_all_posts,
            page=page,
            page_size=page_size,
            db=db
        )
        
        return {
            "status": "success",
            "message": "All posts collection started",
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        logger.error(f"Error starting all posts collection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/collect/all-users")
async def collect_all_users(
    background_tasks: BackgroundTasks,
    page: int = 1,
    page_size: int = 1000,
    flic_token: str = Depends(verify_flic_token),
    db: Session = Depends(get_db)
):
    """
    Collect all users data from the external API.
    """
    try:
        data_collector = DataCollector()
        
        background_tasks.add_task(
            data_collector.collect_all_users,
            page=page,
            page_size=page_size,
            db=db
        )
        
        return {
            "status": "success",
            "message": "All users collection started",
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        logger.error(f"Error starting all users collection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/collection-status")
async def get_collection_status(
    flic_token: str = Depends(verify_flic_token),
    db: Session = Depends(get_db)
):
    """
    Get the status of data collection processes.
    """
    try:
        data_collector = DataCollector()
        status = await data_collector.get_collection_status(db)
        
        return {
            "status": "success",
            "data": status
        }
        
    except Exception as e:
        logger.error(f"Error getting collection status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")