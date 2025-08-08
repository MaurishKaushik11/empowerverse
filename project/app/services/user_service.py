from sqlalchemy.orm import Session
from typing import Optional, Dict, List
import logging

from app.database.models import User, UserInteraction
from app.schemas.recommendation import UserPreferences

logger = logging.getLogger(__name__)

class UserService:
    """
    Service for managing user data and preferences.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_or_create_user(self, username: str) -> User:
        """
        Get existing user or create a new one.
        """
        try:
            # Try to find existing user
            user = self.db.query(User).filter(User.username == username).first()
            
            if user:
                return user
            
            # Create new user
            user = User(
                username=username,
                first_name="",
                last_name="",
                email=f"{username}@example.com",
                picture_url="",
                user_type=None,
                has_evm_wallet=False,
                has_solana_wallet=False,
                preferences=self._get_default_preferences()
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"Created new user: {username}")
            return user
            
        except Exception as e:
            logger.error(f"Error getting or creating user {username}: {str(e)}")
            self.db.rollback()
            raise
    
    async def update_user_preferences(self, user_id: int, preferences: UserPreferences) -> bool:
        """
        Update user preferences.
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                logger.warning(f"User {user_id} not found")
                return False
            
            # Convert preferences to dict
            preferences_dict = {
                "categories": preferences.categories,
                "topics": preferences.topics,
                "mood": preferences.mood,
                "content_types": preferences.content_types
            }
            
            user.preferences = preferences_dict
            self.db.commit()
            
            logger.info(f"Updated preferences for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating user preferences: {str(e)}")
            self.db.rollback()
            return False
    
    async def get_user_interaction_history(self, user_id: int, limit: int = 100) -> List[UserInteraction]:
        """
        Get user's interaction history.
        """
        try:
            interactions = self.db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).order_by(UserInteraction.timestamp.desc()).limit(limit).all()
            
            return interactions
            
        except Exception as e:
            logger.error(f"Error getting user interaction history: {str(e)}")
            return []
    
    async def get_user_stats(self, user_id: int) -> Dict:
        """
        Get user statistics and engagement metrics.
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {}
            
            # Get interaction counts by type
            interaction_counts = self.db.query(
                UserInteraction.interaction_type,
                self.db.func.count(UserInteraction.id)
            ).filter(
                UserInteraction.user_id == user_id
            ).group_by(UserInteraction.interaction_type).all()
            
            interaction_stats = {
                interaction_type: count 
                for interaction_type, count in interaction_counts
            }
            
            # Calculate engagement score
            engagement_score = (
                interaction_stats.get("like", 0) * 2 +
                interaction_stats.get("share", 0) * 3 +
                interaction_stats.get("bookmark", 0) * 2 +
                interaction_stats.get("view", 0) * 1 +
                interaction_stats.get("rate", 0) * 2
            )
            
            total_interactions = sum(interaction_stats.values())
            
            stats = {
                "user_id": user_id,
                "username": user.username,
                "total_interactions": total_interactions,
                "interaction_breakdown": interaction_stats,
                "engagement_score": engagement_score,
                "avg_engagement": engagement_score / max(total_interactions, 1),
                "preferences": user.preferences or {},
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_updated": user.updated_at.isoformat() if user.updated_at else None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {str(e)}")
            return {}
    
    def _get_default_preferences(self) -> Dict:
        """
        Get default user preferences for new users.
        """
        return {
            "categories": ["Motivation", "Education"],
            "topics": ["Personal Growth", "Success Stories"],
            "mood": "energetic",
            "content_types": ["video"]
        }
    
    async def get_similar_users(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Find users with similar preferences and interaction patterns.
        """
        try:
            target_user = self.db.query(User).filter(User.id == user_id).first()
            
            if not target_user:
                return []
            
            target_preferences = target_user.preferences or {}
            target_categories = set(target_preferences.get("categories", []))
            target_topics = set(target_preferences.get("topics", []))
            
            # Find users with similar preferences
            all_users = self.db.query(User).filter(User.id != user_id).all()
            similar_users = []
            
            for user in all_users:
                user_preferences = user.preferences or {}
                user_categories = set(user_preferences.get("categories", []))
                user_topics = set(user_preferences.get("topics", []))
                
                # Calculate similarity score
                category_similarity = len(target_categories & user_categories) / max(len(target_categories | user_categories), 1)
                topic_similarity = len(target_topics & user_topics) / max(len(target_topics | user_topics), 1)
                
                overall_similarity = (category_similarity + topic_similarity) / 2
                
                if overall_similarity > 0.3:  # Threshold for similarity
                    similar_users.append({
                        "user_id": user.id,
                        "username": user.username,
                        "similarity_score": overall_similarity,
                        "common_categories": list(target_categories & user_categories),
                        "common_topics": list(target_topics & user_topics)
                    })
            
            # Sort by similarity score
            similar_users.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return similar_users[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar users: {str(e)}")
            return []