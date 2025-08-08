import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock, patch

from app.main import app
from app.database.database import get_db, Base
from app.database.models import User, Post, Category, Topic, UserInteraction
from app.services.recommendation_engine import RecommendationEngine
from app.schemas.recommendation import FeedRequest

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestRecommendationEndpoints:
    """Test recommendation API endpoints."""
    
    def setup_method(self):
        """Set up test data before each test."""
        self.db = TestingSessionLocal()
        
        # Create test user
        self.test_user = User(
            username="test_user",
            email="test@example.com",
            preferences={"categories": ["Motivation"], "mood": "energetic"}
        )
        self.db.add(self.test_user)
        
        # Create test category
        self.test_category = Category(
            name="Motivation",
            description="Motivational content"
        )
        self.db.add(self.test_category)
        
        # Create test topic
        self.test_topic = Topic(
            name="Personal Growth",
            description="Personal development content",
            slug="personal-growth",
            project_code="motivation"
        )
        self.db.add(self.test_topic)
        
        self.db.commit()
        
        # Create test post
        self.test_post = Post(
            title="Test Motivational Video",
            slug="test-motivational-video",
            owner_id=self.test_user.id,
            category_id=self.test_category.id,
            topic_id=self.test_topic.id,
            video_link="https://example.com/video.mp4",
            thumbnail_url="https://example.com/thumb.jpg",
            view_count=100,
            upvote_count=10,
            average_rating=85
        )
        self.db.add(self.test_post)
        self.db.commit()
    
    def teardown_method(self):
        """Clean up after each test."""
        self.db.query(UserInteraction).delete()
        self.db.query(Post).delete()
        self.db.query(Topic).delete()
        self.db.query(Category).delete()
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_get_personalized_feed(self):
        """Test personalized feed endpoint."""
        response = client.get("/api/v1/feed?username=test_user&page=1&page_size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "post" in data
        assert "algorithm_used" in data
        assert data["page"] == 1
        assert data["page_size"] == 10
    
    def test_get_category_feed(self):
        """Test category-based feed endpoint."""
        response = client.get("/api/v1/feed/category?username=test_user&project_code=motivation")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "post" in data
        assert data["algorithm_used"] == "category_based"
    
    def test_get_trending_content(self):
        """Test trending content endpoint."""
        response = client.get("/api/v1/trending?page=1&page_size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "post" in data
        assert data["algorithm_used"] == "trending"
    
    def test_record_interaction(self):
        """Test recording user interaction."""
        interaction_data = {
            "username": "test_user",
            "post_id": self.test_post.id,
            "interaction_type": "like",
            "interaction_value": 1.0
        }
        
        response = client.post("/api/v1/interaction", json=interaction_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        
        # Verify interaction was recorded
        interaction = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == self.test_user.id,
            UserInteraction.post_id == self.test_post.id,
            UserInteraction.interaction_type == "like"
        ).first()
        assert interaction is not None
    
    def test_get_similar_content(self):
        """Test similar content endpoint."""
        response = client.get(f"/api/v1/similar/{self.test_post.id}?username=test_user")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert data["algorithm_used"] == "content_similarity"
    
    def test_invalid_username(self):
        """Test with invalid username."""
        response = client.get("/api/v1/feed?username=&page=1&page_size=10")
        assert response.status_code == 422  # Validation error
    
    def test_pagination(self):
        """Test pagination parameters."""
        response = client.get("/api/v1/feed?username=test_user&page=2&page_size=5")
        assert response.status_code == 200
        
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 5

class TestRecommendationEngine:
    """Test recommendation engine logic."""
    
    def setup_method(self):
        """Set up test data."""
        self.db = TestingSessionLocal()
        self.engine = RecommendationEngine()
        
        # Create test data
        self.test_user = User(
            username="test_user",
            email="test@example.com",
            preferences={"categories": ["Motivation"], "mood": "energetic"}
        )
        self.db.add(self.test_user)
        self.db.commit()
    
    def teardown_method(self):
        """Clean up after each test."""
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()
    
    @pytest.mark.asyncio
    async def test_get_user_profile(self):
        """Test user profile analysis."""
        profile = await self.engine._get_user_profile(self.test_user.id, self.db)
        
        assert profile["user_id"] == self.test_user.id
        assert "preferences" in profile
        assert "interaction_patterns" in profile
        assert "total_interactions" in profile
    
    @pytest.mark.asyncio
    async def test_cold_start_recommendations(self):
        """Test cold start recommendations."""
        request = FeedRequest(username="new_user", page=1, page_size=10)
        
        recommendations = await self.engine._get_cold_start_recommendations(
            self.test_user.id, request, self.db
        )
        
        assert recommendations.status == "success"
        assert recommendations.algorithm_used == "cold_start_popular"
    
    @pytest.mark.asyncio
    async def test_record_interaction(self):
        """Test recording user interactions."""
        await self.engine.record_interaction(
            self.test_user.id, 1, "like", 1.0, self.db
        )
        
        # Verify interaction was recorded
        interaction = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == self.test_user.id,
            UserInteraction.post_id == 1,
            UserInteraction.interaction_type == "like"
        ).first()
        
        assert interaction is not None
        assert interaction.interaction_value == 1.0

class TestDataCollection:
    """Test data collection endpoints."""
    
    def test_collect_viewed_posts_unauthorized(self):
        """Test data collection without proper token."""
        response = client.post("/api/v1/collect/viewed-posts")
        assert response.status_code == 422  # Missing header
    
    def test_collect_viewed_posts_invalid_token(self):
        """Test data collection with invalid token."""
        headers = {"Flic-Token": "invalid_token"}
        response = client.post("/api/v1/collect/viewed-posts", headers=headers)
        assert response.status_code == 401
    
    @patch('app.services.data_collector.DataCollector.collect_viewed_posts')
    def test_collect_viewed_posts_success(self, mock_collect):
        """Test successful data collection."""
        mock_collect.return_value = 10  # Mock return value
        
        headers = {"Flic-Token": "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"}
        response = client.post("/api/v1/collect/viewed-posts", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data

class TestMLModels:
    """Test machine learning models."""
    
    def setup_method(self):
        """Set up test data."""
        self.engine = RecommendationEngine()
    
    @pytest.mark.asyncio
    async def test_content_embedding_generation(self):
        """Test content embedding generation."""
        user_profile = {
            "user_id": 1,
            "preferences": {"categories": ["Motivation"]},
            "interaction_patterns": {"engagement_score": 0.8},
            "total_interactions": 10
        }
        
        embedding = await self.engine.content_model.generate_user_embedding(user_profile)
        
        assert embedding is not None
        assert len(embedding) == self.engine.content_model.embedding_dim
        assert isinstance(embedding[0], (int, float))
    
    def test_score_combination(self):
        """Test hybrid score combination."""
        deep_scores = [0.8, 0.6, 0.9]
        cf_scores = [0.7, 0.8, 0.5]
        content_scores = [0.6, 0.7, 0.8]
        
        combined = self.engine._combine_scores(deep_scores, cf_scores, content_scores)
        
        assert len(combined) == 3
        assert all(0 <= score <= 1 for score in combined)
        
        # Check that the combination is weighted correctly
        expected_first = 0.8 * 0.5 + 0.7 * 0.3 + 0.6 * 0.2
        assert abs(combined[0] - expected_first) < 0.001

class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_invalid_post_id(self):
        """Test with invalid post ID."""
        response = client.get("/api/v1/similar/999999?username=test_user")
        assert response.status_code == 500  # Internal server error for non-existent post
    
    def test_malformed_interaction_data(self):
        """Test with malformed interaction data."""
        invalid_data = {
            "username": "test_user",
            "post_id": "invalid",  # Should be integer
            "interaction_type": "like"
        }
        
        response = client.post("/api/v1/interaction", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_large_page_size(self):
        """Test with page size exceeding limit."""
        response = client.get("/api/v1/feed?username=test_user&page_size=1000")
        assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__])