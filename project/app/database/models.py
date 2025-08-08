from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    picture_url = Column(String)
    user_type = Column(String)
    has_evm_wallet = Column(Boolean, default=False)
    has_solana_wallet = Column(Boolean, default=False)
    preferences = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interactions = relationship("UserInteraction", back_populates="user")
    embeddings = relationship("UserEmbedding", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    video_link = Column(String)
    thumbnail_url = Column(String)
    gif_thumbnail_url = Column(String)
    view_count = Column(Integer, default=0)
    upvote_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)
    rating_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    is_available_in_public_feed = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User")
    category = relationship("Category", back_populates="posts")
    topic = relationship("Topic", back_populates="posts")
    interactions = relationship("UserInteraction", back_populates="post")
    embeddings = relationship("PostEmbedding", back_populates="post")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    image_url = Column(String)
    count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="category")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    slug = Column(String, unique=True, index=True)
    image_url = Column(String)
    is_public = Column(Boolean, default=True)
    project_code = Column(String)
    posts_count = Column(Integer, default=0)
    language = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User")
    posts = relationship("Post", back_populates="topic")

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    interaction_type = Column(String)  # view, like, bookmark, share, rate
    interaction_value = Column(Float)  # rating value, watch time, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    post = relationship("Post", back_populates="interactions")

class UserEmbedding(Base):
    __tablename__ = "user_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    embedding_vector = Column(JSON)  # Store as JSON array
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="embeddings")

class PostEmbedding(Base):
    __tablename__ = "post_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    content_embedding = Column(JSON)  # Content-based features
    engagement_embedding = Column(JSON)  # Engagement-based features
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="embeddings")

class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommended_posts = Column(JSON)  # List of post IDs
    algorithm_used = Column(String)
    confidence_scores = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")