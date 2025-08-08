from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func
from typing import List, Optional
import logging

from app.database.database import get_db
from app.database.models import User, Post, Category, Topic, UserInteraction, RecommendationLog

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users")
async def get_sample_users(db: Session = Depends(get_db)):
    """Get all sample users for presentation"""
    users = db.query(User).all()
    return {
        "total_users": len(users),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "picture_url": user.picture_url,
                "user_type": user.user_type,
                "has_evm_wallet": user.has_evm_wallet,
                "has_solana_wallet": user.has_solana_wallet,
                "preferences": user.preferences,
                "created_at": user.created_at
            }
            for user in users
        ]
    }

@router.get("/posts")
async def get_sample_posts(
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get sample posts with full details for presentation"""
    query = db.query(Post).options(
        joinedload(Post.owner),
        joinedload(Post.category),
        joinedload(Post.topic)
    ).order_by(desc(Post.view_count))
    
    if category:
        query = query.join(Category).filter(Category.name.ilike(f"%{category}%"))
    
    posts = query.limit(limit).all()
    
    return {
        "total_posts": len(posts),
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "video_link": post.video_link,
                "thumbnail_url": post.thumbnail_url,
                "view_count": post.view_count,
                "upvote_count": post.upvote_count,
                "comment_count": post.comment_count,
                "share_count": post.share_count,
                "bookmark_count": post.bookmark_count,
                "average_rating": post.average_rating,
                "tags": post.tags,
                "created_at": post.created_at,
                "owner": {
                    "username": post.owner.username,
                    "first_name": post.owner.first_name,
                    "last_name": post.owner.last_name,
                    "picture_url": post.owner.picture_url,
                    "user_type": post.owner.user_type
                },
                "category": {
                    "name": post.category.name,
                    "description": post.category.description,
                    "image_url": post.category.image_url
                },
                "topic": {
                    "name": post.topic.name,
                    "description": post.topic.description,
                    "slug": post.topic.slug
                }
            }
            for post in posts
        ]
    }

@router.get("/categories")
async def get_categories_with_stats(db: Session = Depends(get_db)):
    """Get all categories with post counts"""
    categories = db.query(Category).all()
    
    category_stats = []
    for category in categories:
        post_count = db.query(Post).filter(Post.category_id == category.id).count()
        total_views = db.query(func.sum(Post.view_count)).filter(Post.category_id == category.id).scalar() or 0
        
        category_stats.append({
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "image_url": category.image_url,
            "post_count": post_count,
            "total_views": total_views,
            "created_at": category.created_at
        })
    
    return {
        "total_categories": len(categories),
        "categories": category_stats
    }

@router.get("/topics")
async def get_topics_with_stats(db: Session = Depends(get_db)):
    """Get all topics with statistics"""
    topics = db.query(Topic).options(joinedload(Topic.owner)).all()
    
    return {
        "total_topics": len(topics),
        "topics": [
            {
                "id": topic.id,
                "name": topic.name,
                "description": topic.description,
                "slug": topic.slug,
                "image_url": topic.image_url,
                "posts_count": topic.posts_count,
                "language": topic.language,
                "project_code": topic.project_code,
                "owner": {
                    "username": topic.owner.username,
                    "first_name": topic.owner.first_name,
                    "last_name": topic.owner.last_name
                },
                "created_at": topic.created_at
            }
            for topic in topics
        ]
    }

@router.get("/interactions/stats")
async def get_interaction_stats(db: Session = Depends(get_db)):
    """Get interaction statistics for presentation"""
    total_interactions = db.query(UserInteraction).count()
    
    # Interactions by type
    interaction_types = db.query(
        UserInteraction.interaction_type,
        func.count(UserInteraction.id).label('count')
    ).group_by(UserInteraction.interaction_type).all()
    
    # Most active users
    active_users = db.query(
        User.username,
        User.first_name,
        User.last_name,
        User.picture_url,
        func.count(UserInteraction.id).label('interaction_count')
    ).join(UserInteraction).group_by(
        User.id, User.username, User.first_name, User.last_name, User.picture_url
    ).order_by(desc('interaction_count')).limit(5).all()
    
    # Most popular posts
    popular_posts = db.query(
        Post.title,
        Post.thumbnail_url,
        func.count(UserInteraction.id).label('interaction_count'),
        Post.view_count,
        Post.upvote_count
    ).join(UserInteraction).group_by(
        Post.id, Post.title, Post.thumbnail_url, Post.view_count, Post.upvote_count
    ).order_by(desc('interaction_count')).limit(5).all()
    
    return {
        "total_interactions": total_interactions,
        "interaction_types": [
            {"type": interaction_type, "count": count}
            for interaction_type, count in interaction_types
        ],
        "most_active_users": [
            {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "picture_url": picture_url,
                "interaction_count": interaction_count
            }
            for username, first_name, last_name, picture_url, interaction_count in active_users
        ],
        "most_popular_posts": [
            {
                "title": title,
                "thumbnail_url": thumbnail_url,
                "interaction_count": interaction_count,
                "view_count": view_count,
                "upvote_count": upvote_count
            }
            for title, thumbnail_url, interaction_count, view_count, upvote_count in popular_posts
        ]
    }

@router.get("/recommendations/logs")
async def get_recommendation_logs(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get recent recommendation logs for presentation"""
    logs = db.query(RecommendationLog).options(
        joinedload(RecommendationLog.user)
    ).order_by(desc(RecommendationLog.timestamp)).limit(limit).all()
    
    return {
        "total_logs": len(logs),
        "logs": [
            {
                "id": log.id,
                "user": {
                    "username": log.user.username,
                    "first_name": log.user.first_name,
                    "last_name": log.user.last_name
                },
                "algorithm_used": log.algorithm_used,
                "recommended_posts_count": len(log.recommended_posts),
                "average_confidence": sum(log.confidence_scores) / len(log.confidence_scores) if log.confidence_scores else 0,
                "timestamp": log.timestamp
            }
            for log in logs
        ]
    }

@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get comprehensive dashboard statistics for presentation"""
    # Basic counts
    total_users = db.query(User).count()
    total_posts = db.query(Post).count()
    total_categories = db.query(Category).count()
    total_topics = db.query(Topic).count()
    total_interactions = db.query(UserInteraction).count()
    
    # Engagement stats
    total_views = db.query(func.sum(Post.view_count)).scalar() or 0
    total_upvotes = db.query(func.sum(Post.upvote_count)).scalar() or 0
    total_bookmarks = db.query(func.sum(Post.bookmark_count)).scalar() or 0
    total_shares = db.query(func.sum(Post.share_count)).scalar() or 0
    
    # Average ratings
    avg_rating = db.query(func.avg(Post.average_rating)).scalar() or 0
    
    # User types distribution
    user_types = db.query(
        User.user_type,
        func.count(User.id).label('count')
    ).group_by(User.user_type).all()
    
    # Wallet adoption
    evm_users = db.query(User).filter(User.has_evm_wallet == True).count()
    solana_users = db.query(User).filter(User.has_solana_wallet == True).count()
    
    # Recent activity (last 7 days)
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_posts = db.query(Post).filter(Post.created_at >= week_ago).count()
    recent_interactions = db.query(UserInteraction).filter(UserInteraction.timestamp >= week_ago).count()
    
    return {
        "overview": {
            "total_users": total_users,
            "total_posts": total_posts,
            "total_categories": total_categories,
            "total_topics": total_topics,
            "total_interactions": total_interactions
        },
        "engagement": {
            "total_views": total_views,
            "total_upvotes": total_upvotes,
            "total_bookmarks": total_bookmarks,
            "total_shares": total_shares,
            "average_rating": round(avg_rating, 2)
        },
        "user_demographics": {
            "user_types": [
                {"type": user_type, "count": count}
                for user_type, count in user_types
            ],
            "wallet_adoption": {
                "evm_users": evm_users,
                "solana_users": solana_users,
                "total_users": total_users
            }
        },
        "recent_activity": {
            "new_posts_this_week": recent_posts,
            "interactions_this_week": recent_interactions
        }
    }

@router.get("/user/{username}/profile")
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    """Get detailed user profile with activity for presentation"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "User not found"}
    
    # User's posts
    user_posts = db.query(Post).filter(Post.owner_id == user.id).all()
    
    # User's interactions
    user_interactions = db.query(UserInteraction).filter(UserInteraction.user_id == user.id).count()
    
    # User's recent recommendations
    recent_recommendations = db.query(RecommendationLog).filter(
        RecommendationLog.user_id == user.id
    ).order_by(desc(RecommendationLog.timestamp)).limit(3).all()
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "picture_url": user.picture_url,
            "user_type": user.user_type,
            "has_evm_wallet": user.has_evm_wallet,
            "has_solana_wallet": user.has_solana_wallet,
            "preferences": user.preferences,
            "created_at": user.created_at
        },
        "activity": {
            "posts_created": len(user_posts),
            "total_interactions": user_interactions,
            "recent_recommendations": len(recent_recommendations)
        },
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "view_count": post.view_count,
                "upvote_count": post.upvote_count,
                "thumbnail_url": post.thumbnail_url,
                "created_at": post.created_at
            }
            for post in user_posts
        ]
    }