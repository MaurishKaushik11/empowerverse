import httpx
import asyncio
import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
import json

from app.core.config import settings
from app.database.models import User, Post, Category, Topic, UserInteraction
from app.schemas.recommendation import PostResponse

logger = logging.getLogger(__name__)

class DataCollector:
    """
    Service for collecting data from external APIs and storing in database.
    """
    
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.headers = {
            "Flic-Token": settings.FLIC_TOKEN,
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def collect_viewed_posts(self, page: int = 1, page_size: int = 1000, db: Session = None):
        """
        Collect all viewed posts from the external API.
        """
        try:
            url = f"{self.base_url}/posts/view"
            params = {
                "page": page,
                "page_size": page_size,
                "resonance_algorithm": "resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
            }
            
            response = await self.client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success" or data.get("status") == True:
                posts = data.get("post", [])
                
                for post_data in posts:
                    await self._process_post_data(post_data, "view", db)
                
                logger.info(f"Collected {len(posts)} viewed posts from page {page}")
                return len(posts)
            else:
                logger.warning(f"API returned unsuccessful status: {data.get('status')}")
                return 0
                
        except Exception as e:
            logger.error(f"Error collecting viewed posts: {str(e)}")
            return 0
    
    async def collect_liked_posts(self, page: int = 1, page_size: int = 1000, db: Session = None):
        """
        Collect all liked posts from the external API.
        """
        try:
            url = f"{self.base_url}/posts/like"
            params = {
                "page": page,
                "page_size": page_size,
                "resonance_algorithm": "resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
            }
            
            response = await self.client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success" or data.get("status") == True:
                posts = data.get("post", [])
                
                for post_data in posts:
                    await self._process_post_data(post_data, "like", db)
                
                logger.info(f"Collected {len(posts)} liked posts from page {page}")
                return len(posts)
            else:
                logger.warning(f"API returned unsuccessful status: {data.get('status')}")
                return 0
                
        except Exception as e:
            logger.error(f"Error collecting liked posts: {str(e)}")
            return 0
    
    async def collect_inspired_posts(self, page: int = 1, page_size: int = 1000, db: Session = None):
        """
        Collect all inspired posts from the external API.
        """
        try:
            url = f"{self.base_url}/posts/inspire"
            params = {
                "page": page,
                "page_size": page_size,
                "resonance_algorithm": "resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
            }
            
            response = await self.client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success" or data.get("status") == True:
                posts = data.get("post", [])
                
                for post_data in posts:
                    await self._process_post_data(post_data, "inspire", db)
                
                logger.info(f"Collected {len(posts)} inspired posts from page {page}")
                return len(posts)
            else:
                logger.warning(f"API returned unsuccessful status: {data.get('status')}")
                return 0
                
        except Exception as e:
            logger.error(f"Error collecting inspired posts: {str(e)}")
            return 0
    
    async def collect_rated_posts(self, page: int = 1, page_size: int = 1000, db: Session = None):
        """
        Collect all rated posts from the external API.
        """
        try:
            url = f"{self.base_url}/posts/rating"
            params = {
                "page": page,
                "page_size": page_size,
                "resonance_algorithm": "resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
            }
            
            response = await self.client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success" or data.get("status") == True:
                posts = data.get("post", [])
                
                for post_data in posts:
                    await self._process_post_data(post_data, "rate", db)
                
                logger.info(f"Collected {len(posts)} rated posts from page {page}")
                return len(posts)
            else:
                logger.warning(f"API returned unsuccessful status: {data.get('status')}")
                return 0
                
        except Exception as e:
            logger.error(f"Error collecting rated posts: {str(e)}")
            return 0
    
    async def collect_all_posts(self, page: int = 1, page_size: int = 1000, db: Session = None):
        """
        Collect all posts from the external API.
        """
        try:
            url = f"{self.base_url}/posts/summary/get"
            params = {
                "page": page,
                "page_size": page_size
            }
            
            response = await self.client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success" or data.get("status") == True:
                posts = data.get("post", [])
                
                for post_data in posts:
                    await self._process_post_data(post_data, None, db)
                
                logger.info(f"Collected {len(posts)} posts from page {page}")
                return len(posts)
            else:
                logger.warning(f"API returned unsuccessful status: {data.get('status')}")
                return 0
                
        except Exception as e:
            logger.error(f"Error collecting all posts: {str(e)}")
            return 0
    
    async def collect_all_users(self, page: int = 1, page_size: int = 1000, db: Session = None):
        """
        Collect all users from the external API.
        """
        try:
            url = f"{self.base_url}/users/get_all"
            params = {
                "page": page,
                "page_size": page_size
            }
            
            response = await self.client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success" or data.get("status") == True:
                users = data.get("users", [])  # Assuming users are in 'users' field
                
                for user_data in users:
                    await self._process_user_data(user_data, db)
                
                logger.info(f"Collected {len(users)} users from page {page}")
                return len(users)
            else:
                logger.warning(f"API returned unsuccessful status: {data.get('status')}")
                return 0
                
        except Exception as e:
            logger.error(f"Error collecting all users: {str(e)}")
            return 0
    
    async def _process_post_data(self, post_data: Dict, interaction_type: Optional[str], db: Session):
        """
        Process and store post data in the database.
        """
        try:
            if not db:
                logger.warning("No database session provided")
                return
            
            # Extract post information
            post_id = post_data.get("id")
            if not post_id:
                return
            
            # Check if post already exists
            existing_post = db.query(Post).filter(Post.id == post_id).first()
            
            if not existing_post:
                # Create or get category
                category_data = post_data.get("category", {})
                category = await self._get_or_create_category(category_data, db)
                
                # Create or get topic
                topic_data = post_data.get("topic", {})
                topic = await self._get_or_create_topic(topic_data, db)
                
                # Create or get owner
                owner_data = post_data.get("owner", {})
                owner = await self._get_or_create_user(owner_data, db)
                
                # Create post
                post = Post(
                    id=post_id,
                    title=post_data.get("title", ""),
                    slug=post_data.get("slug", ""),
                    owner_id=owner.id if owner else None,
                    category_id=category.id if category else None,
                    topic_id=topic.id if topic else None,
                    video_link=post_data.get("video_link", ""),
                    thumbnail_url=post_data.get("thumbnail_url", ""),
                    gif_thumbnail_url=post_data.get("gif_thumbnail_url"),
                    view_count=post_data.get("view_count", 0),
                    upvote_count=post_data.get("upvote_count", 0),
                    comment_count=post_data.get("comment_count", 0),
                    share_count=post_data.get("share_count", 0),
                    bookmark_count=post_data.get("bookmark_count", 0),
                    rating_count=post_data.get("rating_count", 0),
                    average_rating=post_data.get("average_rating", 0.0),
                    is_available_in_public_feed=post_data.get("is_available_in_public_feed", True),
                    is_locked=post_data.get("is_locked", False),
                    tags=post_data.get("tags", []),
                    created_at=datetime.fromtimestamp(post_data.get("created_at", 0) / 1000) if post_data.get("created_at") else datetime.utcnow()
                )
                
                db.add(post)
                db.commit()
                logger.debug(f"Created post {post_id}")
            else:
                # Update existing post with latest data
                existing_post.view_count = post_data.get("view_count", existing_post.view_count)
                existing_post.upvote_count = post_data.get("upvote_count", existing_post.upvote_count)
                existing_post.comment_count = post_data.get("comment_count", existing_post.comment_count)
                existing_post.share_count = post_data.get("share_count", existing_post.share_count)
                existing_post.bookmark_count = post_data.get("bookmark_count", existing_post.bookmark_count)
                existing_post.rating_count = post_data.get("rating_count", existing_post.rating_count)
                existing_post.average_rating = post_data.get("average_rating", existing_post.average_rating)
                existing_post.updated_at = datetime.utcnow()
                
                db.commit()
                logger.debug(f"Updated post {post_id}")
            
            # Record interaction if specified
            if interaction_type and owner_data:
                owner = await self._get_or_create_user(owner_data, db)
                if owner:
                    await self._record_interaction(owner.id, post_id, interaction_type, db)
                    
        except Exception as e:
            logger.error(f"Error processing post data: {str(e)}")
            if db:
                db.rollback()
    
    async def _process_user_data(self, user_data: Dict, db: Session):
        """
        Process and store user data in the database.
        """
        try:
            if not db:
                return
            
            await self._get_or_create_user(user_data, db)
            
        except Exception as e:
            logger.error(f"Error processing user data: {str(e)}")
            if db:
                db.rollback()
    
    async def _get_or_create_category(self, category_data: Dict, db: Session) -> Optional[Category]:
        """
        Get existing category or create new one.
        """
        try:
            if not category_data or not category_data.get("id"):
                return None
            
            category_id = category_data.get("id")
            category = db.query(Category).filter(Category.id == category_id).first()
            
            if not category:
                category = Category(
                    id=category_id,
                    name=category_data.get("name", ""),
                    description=category_data.get("description", ""),
                    image_url=category_data.get("image_url", ""),
                    count=category_data.get("count", 0)
                )
                db.add(category)
                db.commit()
                logger.debug(f"Created category {category_id}")
            
            return category
            
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            return None
    
    async def _get_or_create_topic(self, topic_data: Dict, db: Session) -> Optional[Topic]:
        """
        Get existing topic or create new one.
        """
        try:
            if not topic_data or not topic_data.get("id"):
                return None
            
            topic_id = topic_data.get("id")
            topic = db.query(Topic).filter(Topic.id == topic_id).first()
            
            if not topic:
                # Get or create topic owner
                owner_data = topic_data.get("owner", {})
                owner = await self._get_or_create_user(owner_data, db) if owner_data else None
                
                topic = Topic(
                    id=topic_id,
                    name=topic_data.get("name", ""),
                    description=topic_data.get("description", ""),
                    slug=topic_data.get("slug", ""),
                    image_url=topic_data.get("image_url", ""),
                    is_public=topic_data.get("is_public", True),
                    project_code=topic_data.get("project_code", ""),
                    posts_count=topic_data.get("posts_count", 0),
                    language=topic_data.get("language"),
                    owner_id=owner.id if owner else None,
                    created_at=datetime.strptime(topic_data.get("created_at", ""), "%Y-%m-%d %H:%M:%S") if topic_data.get("created_at") else datetime.utcnow()
                )
                db.add(topic)
                db.commit()
                logger.debug(f"Created topic {topic_id}")
            
            return topic
            
        except Exception as e:
            logger.error(f"Error creating topic: {str(e)}")
            return None
    
    async def _get_or_create_user(self, user_data: Dict, db: Session) -> Optional[User]:
        """
        Get existing user or create new one.
        """
        try:
            if not user_data or not user_data.get("username"):
                return None
            
            username = user_data.get("username")
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                user = User(
                    username=username,
                    first_name=user_data.get("first_name", ""),
                    last_name=user_data.get("last_name", ""),
                    email=user_data.get("email", f"{username}@example.com"),  # Default email
                    picture_url=user_data.get("picture_url", ""),
                    user_type=user_data.get("user_type"),
                    has_evm_wallet=user_data.get("has_evm_wallet", False),
                    has_solana_wallet=user_data.get("has_solana_wallet", False),
                    preferences={}
                )
                db.add(user)
                db.commit()
                logger.debug(f"Created user {username}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None
    
    async def _record_interaction(self, user_id: int, post_id: int, interaction_type: str, db: Session):
        """
        Record user interaction with a post.
        """
        try:
            # Check if interaction already exists
            existing_interaction = db.query(UserInteraction).filter(
                and_(
                    UserInteraction.user_id == user_id,
                    UserInteraction.post_id == post_id,
                    UserInteraction.interaction_type == interaction_type
                )
            ).first()
            
            if not existing_interaction:
                interaction = UserInteraction(
                    user_id=user_id,
                    post_id=post_id,
                    interaction_type=interaction_type,
                    interaction_value=1.0,
                    timestamp=datetime.utcnow()
                )
                db.add(interaction)
                db.commit()
                logger.debug(f"Recorded {interaction_type} interaction for user {user_id} on post {post_id}")
                
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")
    
    async def get_collection_status(self, db: Session) -> Dict:
        """
        Get the status of data collection.
        """
        try:
            status = {
                "total_users": db.query(User).count(),
                "total_posts": db.query(Post).count(),
                "total_categories": db.query(Category).count(),
                "total_topics": db.query(Topic).count(),
                "total_interactions": db.query(UserInteraction).count(),
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Get interaction type breakdown
            interaction_types = db.query(
                UserInteraction.interaction_type,
                db.func.count(UserInteraction.id)
            ).group_by(UserInteraction.interaction_type).all()
            
            status["interaction_breakdown"] = {
                interaction_type: count for interaction_type, count in interaction_types
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting collection status: {str(e)}")
            return {"error": str(e)}
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()