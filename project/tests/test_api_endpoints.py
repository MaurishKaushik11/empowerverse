import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.database import get_db, Base
from app.database.models import User, Post, Category, Topic

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_data():
    db = TestingSessionLocal()
    
    # Create test category
    category = Category(
        id=1,
        name="Test Category",
        description="Test category description",
        count=10
    )
    db.add(category)
    
    # Create test topic
    topic = Topic(
        id=1,
        name="Test Topic",
        description="Test topic description",
        slug="test-topic",
        project_code="test",
        posts_count=5
    )
    db.add(topic)
    
    # Create test user
    user = User(
        id=1,
        username="testuser",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        preferences={"categories": ["Test Category"], "mood": "energetic"}
    )
    db.add(user)
    
    # Create test posts
    for i in range(5):
        post = Post(
            id=i+1,
            title=f"Test Post {i+1}",
            slug=f"test-post-{i+1}",
            owner_id=1,
            category_id=1,
            topic_id=1,
            video_link="https://example.com/video.mp4",
            thumbnail_url="https://example.com/thumb.jpg",
            view_count=100 * (i+1),
            upvote_count=10 * (i+1),
            comment_count=5 * (i+1),
            tags=["test", "video"]
        )
        db.add(post)
    
    db.commit()
    db.close()

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Video Recommendation Engine API"
    assert data["version"] == "1.0.0"

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "video-recommendation-engine"

def test_personalized_feed(client, sample_data):
    response = client.get("/api/v1/feed?username=testuser&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "post" in data
    assert "algorithm_used" in data

def test_category_feed(client, sample_data):
    response = client.get("/api/v1/feed/category?username=testuser&project_code=test&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "post" in data

def test_trending_content(client, sample_data):
    response = client.get("/api/v1/trending?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "post" in data

def test_similar_content(client, sample_data):
    response = client.get("/api/v1/similar/1?username=testuser&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "post" in data

def test_record_interaction(client, sample_data):
    interaction_data = {
        "username": "testuser",
        "post_id": 1,
        "interaction_type": "like",
        "interaction_value": 1.0
    }
    response = client.post("/api/v1/interaction", json=interaction_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_invalid_username_feed(client):
    response = client.get("/api/v1/feed?username=&page=1&page_size=10")
    assert response.status_code == 422  # Validation error

def test_invalid_page_parameters(client):
    response = client.get("/api/v1/feed?username=testuser&page=0&page_size=10")
    assert response.status_code == 422  # Validation error

def test_large_page_size(client):
    response = client.get("/api/v1/feed?username=testuser&page=1&page_size=1000")
    assert response.status_code == 422  # Should exceed max page size

if __name__ == "__main__":
    pytest.main([__file__])