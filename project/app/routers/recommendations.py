from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import logging

from app.database.database import get_db
from app.schemas.recommendation import RecommendationResponse, FeedRequest, InteractionRequest
from app.services.recommendation_engine import RecommendationEngine
from app.services.user_service import UserService
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/feed", response_model=RecommendationResponse)
async def get_personalized_feed(
    username: str = Query(..., description="Username for personalized recommendations"),
    project_code: Optional[str] = Query(None, description="Category/project code filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    mood: Optional[str] = Query(None, description="Mood filter"),
    category: Optional[str] = Query(None, description="Category filter"),
    db: Session = Depends(get_db)
):
    """
    Get personalized video recommendations for a specific user.
    
    This endpoint uses deep neural networks and collaborative filtering
    to provide highly personalized content recommendations.
    """
    try:
        # Initialize services
        recommendation_engine = RecommendationEngine()
        user_service = UserService(db)
        
        # Get or create user
        user = await user_service.get_or_create_user(username)
        
        # Prepare request
        feed_request = FeedRequest(
            username=username,
            project_code=project_code,
            page=page,
            page_size=page_size,
            mood=mood,
            category=category
        )
        
        # Get recommendations
        recommendations = await recommendation_engine.get_personalized_recommendations(
            user_id=user.id,
            request=feed_request,
            db=db
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting personalized feed for {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/feed/category", response_model=RecommendationResponse)
async def get_category_based_feed(
    username: str = Query(..., description="Username for recommendations"),
    project_code: str = Query(..., description="Project/category code"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Get category-specific video recommendations for a user.
    
    Returns recommendations filtered by specific category/project code
    while still considering user preferences.
    """
    try:
        recommendation_engine = RecommendationEngine()
        user_service = UserService(db)
        
        user = await user_service.get_or_create_user(username)
        
        feed_request = FeedRequest(
            username=username,
            project_code=project_code,
            page=page,
            page_size=page_size
        )
        
        recommendations = await recommendation_engine.get_category_recommendations(
            user_id=user.id,
            request=feed_request,
            db=db
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting category feed for {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/interaction")
async def record_user_interaction(
    interaction: InteractionRequest,
    db: Session = Depends(get_db)
):
    """
    Record user interaction with a post for improving recommendations.
    
    Interactions include: view, like, bookmark, share, rate
    """
    try:
        recommendation_engine = RecommendationEngine()
        user_service = UserService(db)
        
        user = await user_service.get_or_create_user(interaction.username)
        
        # Record interaction
        await recommendation_engine.record_interaction(
            user_id=user.id,
            post_id=interaction.post_id,
            interaction_type=interaction.interaction_type,
            interaction_value=interaction.interaction_value,
            db=db
        )
        
        return {"status": "success", "message": "Interaction recorded"}
        
    except Exception as e:
        logger.error(f"Error recording interaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/trending", response_model=RecommendationResponse)
async def get_trending_content(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    category: Optional[str] = Query(None, description="Category filter"),
    db: Session = Depends(get_db)
):
    """
    Get trending video content based on engagement metrics.
    """
    try:
        recommendation_engine = RecommendationEngine()
        
        recommendations = await recommendation_engine.get_trending_content(
            page=page,
            page_size=page_size,
            category=category,
            db=db
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting trending content: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/similar/{post_id}", response_model=RecommendationResponse)
async def get_similar_content(
    post_id: int,
    username: Optional[str] = Query(None, description="Username for personalization"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Get content similar to a specific post using content-based filtering.
    """
    try:
        recommendation_engine = RecommendationEngine()
        user_id = None
        
        if username:
            user_service = UserService(db)
            user = await user_service.get_or_create_user(username)
            user_id = user.id
        
        recommendations = await recommendation_engine.get_similar_content(
            post_id=post_id,
            user_id=user_id,
            page=page,
            page_size=page_size,
            db=db
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting similar content for post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")