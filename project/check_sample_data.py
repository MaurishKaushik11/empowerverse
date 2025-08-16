import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import User, Post, UserInteraction, Base

# Use PostgreSQL from config
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/video_recommendation_db"
engine = create_engine(DATABASE_URL, echo=False)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def check_data():
    """Check sample data for users and posts"""
    users = db.query(User).all()
    posts = db.query(Post).all()
    
    print("Sample Users:")
    for user in users:
        print(f"Username: {user.username}, Email: {user.email}")

    print("\nSample Posts:")
    for post in posts:
        print(f"Title: {post.title}, Owner: {post.owner_id}")

if __name__ == "__main__":
    check_data()
    db.close()
