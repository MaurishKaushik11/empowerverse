import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
import logging
from datetime import datetime, timedelta
import json

from app.database.models import User, Post, UserInteraction, UserEmbedding, PostEmbedding, RecommendationLog
from app.schemas.recommendation import RecommendationResponse, FeedRequest, PostResponse
from app.services.neural_networks import DeepRecommendationModel, ContentEmbeddingModel
from app.services.collaborative_filtering import CollaborativeFilter
from app.core.config import settings

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.deep_model = DeepRecommendationModel()
        self.content_model = ContentEmbeddingModel()
        self.collaborative_filter = CollaborativeFilter()
        self.model_version = "v1.0"
        
    async def get_personalized_recommendations(
        self, 
        user_id: int, 
        request: FeedRequest, 
        db: Session
    ) -> RecommendationResponse:
        """
        Get personalized recommendations using deep neural networks and hybrid filtering.
        """
        try:
            # Get user profile and interaction history
            user_profile = await self._get_user_profile(user_id, db)
            
            # Check if user has enough interaction history
            interaction_count = db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).count()
            
            if interaction_count < settings.COLD_START_THRESHOLD:
                # Handle cold start problem
                return await self._get_cold_start_recommendations(user_id, request, db)
            
            # Get candidate posts
            candidate_posts = await self._get_candidate_posts(request, db)
            
            # Generate embeddings for user and posts
            user_embedding = await self._get_or_generate_user_embedding(user_id, db)
            post_embeddings = await self._get_or_generate_post_embeddings(candidate_posts, db)
            
            # Deep learning recommendations
            deep_scores = await self.deep_model.predict(
                user_embedding, 
                post_embeddings, 
                user_profile
            )
            
            # Collaborative filtering scores
            cf_scores = await self.collaborative_filter.get_user_similarities(
                user_id, 
                [post.id for post in candidate_posts], 
                db
            )
            
            # Content-based scores
            content_scores = await self._get_content_based_scores(
                user_profile, 
                candidate_posts
            )
            
            # Hybrid scoring (weighted combination)
            final_scores = self._combine_scores(deep_scores, cf_scores, content_scores)
            
            # Rank and filter posts
            ranked_posts = self._rank_posts(candidate_posts, final_scores)
            
            # Apply pagination
            start_idx = (request.page - 1) * request.page_size
            end_idx = start_idx + request.page_size
            paginated_posts = ranked_posts[start_idx:end_idx]
            
            # Convert to response format
            post_responses = [self._convert_to_post_response(post) for post in paginated_posts]
            
            # Log recommendation
            await self._log_recommendation(
                user_id, 
                [post.id for post in paginated_posts], 
                "hybrid_deep_learning",
                final_scores[start_idx:end_idx],
                db
            )
            
            return RecommendationResponse(
                status="success",
                post=post_responses,
                algorithm_used="hybrid_deep_learning",
                total_count=len(ranked_posts),
                page=request.page,
                page_size=request.page_size,
                confidence_scores=final_scores[start_idx:end_idx]
            )
            
        except Exception as e:
            logger.error(f"Error in personalized recommendations: {str(e)}")
            # Fallback to trending content
            return await self.get_trending_content(request.page, request.page_size, None, db)
    
    async def get_category_recommendations(
        self, 
        user_id: int, 
        request: FeedRequest, 
        db: Session
    ) -> RecommendationResponse:
        """
        Get category-specific recommendations while considering user preferences.
        """
        try:
            # Filter posts by category/project_code
            query = db.query(Post).filter(
                and_(
                    Post.is_available_in_public_feed == True,
                    Post.is_locked == False
                )
            )
            
            if request.project_code:
                # Join with topic to filter by project_code
                query = query.join(Post.topic).filter(
                    Post.topic.has(project_code=request.project_code)
                )
            
            candidate_posts = query.all()
            
            # Get user preferences for personalization
            user_profile = await self._get_user_profile(user_id, db)
            
            # Score posts based on user preferences and category relevance
            scores = await self._score_category_posts(user_profile, candidate_posts)
            
            # Rank posts
            ranked_posts = self._rank_posts(candidate_posts, scores)
            
            # Apply pagination
            start_idx = (request.page - 1) * request.page_size
            end_idx = start_idx + request.page_size
            paginated_posts = ranked_posts[start_idx:end_idx]
            
            post_responses = [self._convert_to_post_response(post) for post in paginated_posts]
            
            return RecommendationResponse(
                status="success",
                post=post_responses,
                algorithm_used="category_based",
                total_count=len(ranked_posts),
                page=request.page,
                page_size=request.page_size
            )
            
        except Exception as e:
            logger.error(f"Error in category recommendations: {str(e)}")
            raise
    
    async def get_trending_content(
        self, 
        page: int, 
        page_size: int, 
        category: Optional[str], 
        db: Session
    ) -> RecommendationResponse:
        """
        Get trending content based on engagement metrics.
        """
        try:
            # Calculate trending score based on recent engagement
            recent_date = datetime.utcnow() - timedelta(days=7)
            
            query = db.query(Post).filter(
                and_(
                    Post.is_available_in_public_feed == True,
                    Post.is_locked == False,
                    Post.created_at >= recent_date
                )
            )
            
            if category:
                query = query.join(Post.category).filter(
                    Post.category.has(name=category)
                )
            
            # Order by trending score (combination of views, likes, shares, recency)
            posts = query.order_by(
                desc(
                    (Post.view_count * 0.3 + 
                     Post.upvote_count * 0.4 + 
                     Post.share_count * 0.3) / 
                    func.extract('epoch', func.now() - Post.created_at) * 86400
                )
            ).offset((page - 1) * page_size).limit(page_size).all()
            
            post_responses = [self._convert_to_post_response(post) for post in posts]
            
            return RecommendationResponse(
                status="success",
                post=post_responses,
                algorithm_used="trending",
                total_count=len(posts),
                page=page,
                page_size=page_size
            )
            
        except Exception as e:
            logger.error(f"Error getting trending content: {str(e)}")
            raise
    
    async def get_similar_content(
        self, 
        post_id: int, 
        user_id: Optional[int], 
        page: int, 
        page_size: int, 
        db: Session
    ) -> RecommendationResponse:
        """
        Get content similar to a specific post using content-based filtering.
        """
        try:
            # Get the reference post
            reference_post = db.query(Post).filter(Post.id == post_id).first()
            if not reference_post:
                raise ValueError(f"Post {post_id} not found")
            
            # Get post embedding
            reference_embedding = await self._get_or_generate_post_embeddings([reference_post], db)
            
            # Find similar posts using content embeddings
            candidate_posts = db.query(Post).filter(
                and_(
                    Post.id != post_id,
                    Post.is_available_in_public_feed == True,
                    Post.is_locked == False
                )
            ).all()
            
            candidate_embeddings = await self._get_or_generate_post_embeddings(candidate_posts, db)
            
            # Calculate similarity scores
            similarity_scores = self._calculate_cosine_similarity(
                reference_embedding[0], 
                candidate_embeddings
            )
            
            # Filter by similarity threshold
            similar_posts = [
                (post, score) for post, score in zip(candidate_posts, similarity_scores)
                if score >= settings.SIMILARITY_THRESHOLD
            ]
            
            # Sort by similarity score
            similar_posts.sort(key=lambda x: x[1], reverse=True)
            
            # Apply pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_posts = similar_posts[start_idx:end_idx]
            
            post_responses = [
                self._convert_to_post_response(post) 
                for post, _ in paginated_posts
            ]
            
            return RecommendationResponse(
                status="success",
                post=post_responses,
                algorithm_used="content_similarity",
                total_count=len(similar_posts),
                page=page,
                page_size=page_size,
                confidence_scores=[score for _, score in paginated_posts]
            )
            
        except Exception as e:
            logger.error(f"Error getting similar content: {str(e)}")
            raise
    
    async def record_interaction(
        self, 
        user_id: int, 
        post_id: int, 
        interaction_type: str, 
        interaction_value: Optional[float], 
        db: Session
    ):
        """
        Record user interaction and update embeddings.
        """
        try:
            # Create interaction record
            interaction = UserInteraction(
                user_id=user_id,
                post_id=post_id,
                interaction_type=interaction_type,
                interaction_value=interaction_value or 1.0,
                timestamp=datetime.utcnow()
            )
            
            db.add(interaction)
            db.commit()
            
            # Update user embedding asynchronously
            await self._update_user_embedding(user_id, db)
            
            logger.info(f"Recorded {interaction_type} interaction for user {user_id} on post {post_id}")
            
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")
            db.rollback()
            raise
    
    # Private helper methods
    
    async def _get_user_profile(self, user_id: int, db: Session) -> Dict:
        """Get comprehensive user profile including preferences and interaction history."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}
        
        # Get interaction history
        interactions = db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).order_by(desc(UserInteraction.timestamp)).limit(100).all()
        
        # Analyze interaction patterns
        interaction_patterns = self._analyze_interaction_patterns(interactions)
        
        return {
            "user_id": user_id,
            "preferences": user.preferences or {},
            "interaction_patterns": interaction_patterns,
            "total_interactions": len(interactions)
        }
    
    async def _get_cold_start_recommendations(
        self, 
        user_id: int, 
        request: FeedRequest, 
        db: Session
    ) -> RecommendationResponse:
        """Handle cold start problem with mood-based and popular content."""
        try:
            # Get popular content from the last week
            recent_date = datetime.utcnow() - timedelta(days=7)
            
            query = db.query(Post).filter(
                and_(
                    Post.is_available_in_public_feed == True,
                    Post.is_locked == False,
                    Post.created_at >= recent_date
                )
            )
            
            # Apply mood filter if specified
            if request.mood:
                # This would require a mood field in the Post model
                # For now, we'll use category as a proxy
                pass
            
            # Order by engagement score
            posts = query.order_by(
                desc(Post.view_count + Post.upvote_count * 2 + Post.share_count * 3)
            ).offset((request.page - 1) * request.page_size).limit(request.page_size).all()
            
            post_responses = [self._convert_to_post_response(post) for post in posts]
            
            return RecommendationResponse(
                status="success",
                post=post_responses,
                algorithm_used="cold_start_popular",
                total_count=len(posts),
                page=request.page,
                page_size=request.page_size
            )
            
        except Exception as e:
            logger.error(f"Error in cold start recommendations: {str(e)}")
            raise
    
    async def _get_candidate_posts(self, request: FeedRequest, db: Session) -> List[Post]:
        """Get candidate posts for recommendation."""
        query = db.query(Post).filter(
            and_(
                Post.is_available_in_public_feed == True,
                Post.is_locked == False
            )
        )
        
        # Apply filters
        if request.project_code:
            query = query.join(Post.topic).filter(
                Post.topic.has(project_code=request.project_code)
            )
        
        if request.category:
            query = query.join(Post.category).filter(
                Post.category.has(name=request.category)
            )
        
        return query.limit(settings.MAX_RECOMMENDATIONS * 2).all()
    
    async def _get_or_generate_user_embedding(self, user_id: int, db: Session) -> np.ndarray:
        """Get or generate user embedding vector."""
        # Check if embedding exists
        embedding_record = db.query(UserEmbedding).filter(
            and_(
                UserEmbedding.user_id == user_id,
                UserEmbedding.model_version == self.model_version
            )
        ).first()
        
        if embedding_record:
            return np.array(embedding_record.embedding_vector)
        
        # Generate new embedding
        user_profile = await self._get_user_profile(user_id, db)
        embedding = await self.content_model.generate_user_embedding(user_profile)
        
        # Save embedding
        embedding_record = UserEmbedding(
            user_id=user_id,
            embedding_vector=embedding.tolist(),
            model_version=self.model_version
        )
        db.add(embedding_record)
        db.commit()
        
        return embedding
    
    async def _get_or_generate_post_embeddings(self, posts: List[Post], db: Session) -> List[np.ndarray]:
        """Get or generate post embedding vectors."""
        embeddings = []
        
        for post in posts:
            # Check if embedding exists
            embedding_record = db.query(PostEmbedding).filter(
                and_(
                    PostEmbedding.post_id == post.id,
                    PostEmbedding.model_version == self.model_version
                )
            ).first()
            
            if embedding_record:
                embeddings.append(np.array(embedding_record.content_embedding))
            else:
                # Generate new embedding
                embedding = await self.content_model.generate_post_embedding(post)
                
                # Save embedding
                embedding_record = PostEmbedding(
                    post_id=post.id,
                    content_embedding=embedding.tolist(),
                    model_version=self.model_version
                )
                db.add(embedding_record)
                embeddings.append(embedding)
        
        db.commit()
        return embeddings
    
    def _combine_scores(
        self, 
        deep_scores: List[float], 
        cf_scores: List[float], 
        content_scores: List[float]
    ) -> List[float]:
        """Combine different recommendation scores using weighted average."""
        weights = {
            'deep': 0.5,
            'collaborative': 0.3,
            'content': 0.2
        }
        
        combined_scores = []
        for i in range(len(deep_scores)):
            score = (
                deep_scores[i] * weights['deep'] +
                cf_scores[i] * weights['collaborative'] +
                content_scores[i] * weights['content']
            )
            combined_scores.append(score)
        
        return combined_scores
    
    def _rank_posts(self, posts: List[Post], scores: List[float]) -> List[Post]:
        """Rank posts by their scores."""
        post_score_pairs = list(zip(posts, scores))
        post_score_pairs.sort(key=lambda x: x[1], reverse=True)
        return [post for post, _ in post_score_pairs]
    
    def _convert_to_post_response(self, post: Post) -> PostResponse:
        """Convert database Post model to API response format."""
        return PostResponse(
            id=post.id,
            title=post.title,
            slug=post.slug,
            owner={
                "first_name": post.owner.first_name or "",
                "last_name": post.owner.last_name or "",
                "name": f"{post.owner.first_name or ''} {post.owner.last_name or ''}".strip(),
                "username": post.owner.username,
                "picture_url": post.owner.picture_url or "",
                "user_type": post.owner.user_type,
                "has_evm_wallet": post.owner.has_evm_wallet,
                "has_solana_wallet": post.owner.has_solana_wallet
            },
            category={
                "id": post.category.id,
                "name": post.category.name,
                "count": post.category.count,
                "description": post.category.description or "",
                "image_url": post.category.image_url or ""
            },
            topic={
                "id": post.topic.id,
                "name": post.topic.name,
                "description": post.topic.description or "",
                "image_url": post.topic.image_url or "",
                "slug": post.topic.slug,
                "is_public": post.topic.is_public,
                "project_code": post.topic.project_code or "",
                "posts_count": post.topic.posts_count,
                "language": post.topic.language,
                "created_at": post.topic.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "owner": {
                    "first_name": post.topic.owner.first_name or "",
                    "last_name": post.topic.owner.last_name or "",
                    "name": f"{post.topic.owner.first_name or ''} {post.topic.owner.last_name or ''}".strip(),
                    "username": post.topic.owner.username,
                    "profile_url": post.topic.owner.picture_url or "",
                    "user_type": post.topic.owner.user_type or ""
                }
            },
            video_link=post.video_link or "",
            thumbnail_url=post.thumbnail_url or "",
            gif_thumbnail_url=post.gif_thumbnail_url,
            view_count=post.view_count,
            upvote_count=post.upvote_count,
            comment_count=post.comment_count,
            share_count=post.share_count,
            bookmark_count=post.bookmark_count,
            rating_count=post.rating_count,
            average_rating=post.average_rating,
            is_available_in_public_feed=post.is_available_in_public_feed,
            is_locked=post.is_locked,
            tags=post.tags or [],
            created_at=int(post.created_at.timestamp() * 1000),
            identifier=post.slug[:7],  # Generate identifier from slug
            exit_count=0,  # Default value
            contract_address="",
            chain_id="",
            chart_url="",
            baseToken={}
        )
    
    async def _log_recommendation(
        self, 
        user_id: int, 
        post_ids: List[int], 
        algorithm: str, 
        scores: List[float], 
        db: Session
    ):
        """Log recommendation for analysis and improvement."""
        try:
            log_entry = RecommendationLog(
                user_id=user_id,
                recommended_posts=post_ids,
                algorithm_used=algorithm,
                confidence_scores=scores,
                timestamp=datetime.utcnow()
            )
            
            db.add(log_entry)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error logging recommendation: {str(e)}")
    
    def _analyze_interaction_patterns(self, interactions: List[UserInteraction]) -> Dict:
        """Analyze user interaction patterns for better recommendations."""
        if not interactions:
            return {}
        
        patterns = {
            "most_interacted_categories": {},
            "interaction_types": {},
            "time_patterns": {},
            "engagement_score": 0
        }
        
        # Analyze interaction types
        for interaction in interactions:
            interaction_type = interaction.interaction_type
            patterns["interaction_types"][interaction_type] = patterns["interaction_types"].get(interaction_type, 0) + 1
        
        # Calculate engagement score
        total_interactions = len(interactions)
        like_weight = 2
        share_weight = 3
        bookmark_weight = 2
        view_weight = 1
        
        engagement_score = (
            patterns["interaction_types"].get("like", 0) * like_weight +
            patterns["interaction_types"].get("share", 0) * share_weight +
            patterns["interaction_types"].get("bookmark", 0) * bookmark_weight +
            patterns["interaction_types"].get("view", 0) * view_weight
        ) / max(total_interactions, 1)
        
        patterns["engagement_score"] = engagement_score
        
        return patterns
    
    async def _get_content_based_scores(self, user_profile: Dict, posts: List[Post]) -> List[float]:
        """Calculate content-based recommendation scores."""
        scores = []
        
        for post in posts:
            score = 0.0
            
            # Category preference
            user_prefs = user_profile.get("preferences", {})
            preferred_categories = user_prefs.get("categories", [])
            if post.category.name in preferred_categories:
                score += 2.0
            
            # Engagement metrics
            score += np.log(post.view_count + 1) / 10
            score += np.log(post.upvote_count + 1) / 5
            score += post.average_rating / 25
            
            # Recency boost
            days_old = (datetime.utcnow() - post.created_at).days
            if days_old < 7:
                score += 1.0
            elif days_old < 30:
                score += 0.5
            
            scores.append(score)
        
        return scores
    
    async def _score_category_posts(self, user_profile: Dict, posts: List[Post]) -> List[float]:
        """Score posts within a specific category."""
        scores = []
        
        for post in posts:
            score = 0.0
            
            # Base engagement score
            score += np.log(post.view_count + 1) / 10
            score += np.log(post.upvote_count + 1) / 5
            score += post.average_rating / 25
            
            # User interaction history bonus
            interaction_patterns = user_profile.get("interaction_patterns", {})
            engagement_score = interaction_patterns.get("engagement_score", 0)
            score += engagement_score
            
            # Recency factor
            days_old = (datetime.utcnow() - post.created_at).days
            recency_factor = max(0, 1 - days_old / 30)  # Decay over 30 days
            score *= (1 + recency_factor)
            
            scores.append(score)
        
        return scores
    
    def _calculate_cosine_similarity(self, vec1: np.ndarray, vec_list: List[np.ndarray]) -> List[float]:
        """Calculate cosine similarity between one vector and a list of vectors."""
        similarities = []
        
        for vec2 in vec_list:
            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                similarity = 0.0
            else:
                similarity = dot_product / (norm1 * norm2)
            
            similarities.append(similarity)
        
        return similarities
    
    async def _update_user_embedding(self, user_id: int, db: Session):
        """Update user embedding based on recent interactions."""
        try:
            # Get recent interactions
            recent_interactions = db.query(UserInteraction).filter(
                and_(
                    UserInteraction.user_id == user_id,
                    UserInteraction.timestamp >= datetime.utcnow() - timedelta(days=30)
                )
            ).all()
            
            if len(recent_interactions) < 5:
                return  # Not enough data for update
            
            # Generate new embedding
            user_profile = await self._get_user_profile(user_id, db)
            new_embedding = await self.content_model.generate_user_embedding(user_profile)
            
            # Update or create embedding record
            embedding_record = db.query(UserEmbedding).filter(
                and_(
                    UserEmbedding.user_id == user_id,
                    UserEmbedding.model_version == self.model_version
                )
            ).first()
            
            if embedding_record:
                embedding_record.embedding_vector = new_embedding.tolist()
                embedding_record.updated_at = datetime.utcnow()
            else:
                embedding_record = UserEmbedding(
                    user_id=user_id,
                    embedding_vector=new_embedding.tolist(),
                    model_version=self.model_version
                )
                db.add(embedding_record)
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error updating user embedding: {str(e)}")
            db.rollback()