from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    interactions = relationship("Interaction", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    view_count = Column(Integer, default=0)
    upvote_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    rating_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    share_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)
    is_available_in_public_feed = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    video_link = Column(String)
    thumbnail_url = Column(String)
    gif_thumbnail_url = Column(String)
    tags = Column(JSON)
    created_at_ms = Column(Integer)
    owner = Column(JSON)
    category = Column(JSON)
    topic = Column(JSON)
    base_token = Column(JSON)
    project_code = Column(String)  # Add project_code field
    interactions = relationship("Interaction", back_populates="post")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    type = Column(String, nullable=False)
    value = Column(Float, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    user = relationship("User", back_populates="interactions")
    post = relationship("Post", back_populates="interactions")