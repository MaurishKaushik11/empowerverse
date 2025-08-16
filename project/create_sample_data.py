#!/usr/bin/env python3
"""
Create sample data for testing the recommendation system
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from dotenv import load_dotenv
from app.database.database import SessionLocal
from app.database import models
import json

def create_sample_data():
    """Create sample users, posts, and interactions"""
    db = SessionLocal()
    
    try:
        # Create sample users
        users_data = [
            {"username": "alice"},
            {"username": "bob"},
            {"username": "charlie"},
            {"username": "diana"},
            {"username": "eve"}
        ]
        
        users = []
        for user_data in users_data:
            user = models.User(**user_data)
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"Created {len(users)} users")
        
        # Create sample posts
        posts_data = [
            {
                "title": "Introduction to Machine Learning",
                "slug": "intro-ml",
                "view_count": 150,
                "upvote_count": 25,
                "bookmark_count": 10,
                "rating_count": 8,
                "average_rating": 4.5,
                "tags": ["machine learning", "ai", "tutorial"],
                "category": {"name": "education", "id": 1},
                "topic": {"name": "AI & ML", "project_code": "EV"},
                "project_code": "EV",
                "video_link": "https://example.com/video1.mp4",
                "thumbnail_url": "https://example.com/thumb1.jpg"
            },
            {
                "title": "Fitness Motivation Tips",
                "slug": "fitness-motivation",
                "view_count": 200,
                "upvote_count": 35,
                "bookmark_count": 15,
                "rating_count": 12,
                "average_rating": 4.2,
                "tags": ["fitness", "motivation", "health"],
                "category": {"name": "fitness", "id": 2},
                "topic": {"name": "Health & Fitness", "project_code": "FIT"},
                "project_code": "FIT",
                "video_link": "https://example.com/video2.mp4",
                "thumbnail_url": "https://example.com/thumb2.jpg"
            },
            {
                "title": "Cooking Basics for Beginners",
                "slug": "cooking-basics",
                "view_count": 120,
                "upvote_count": 20,
                "bookmark_count": 8,
                "rating_count": 6,
                "average_rating": 4.0,
                "tags": ["cooking", "tutorial", "beginner"],
                "category": {"name": "lifestyle", "id": 3},
                "topic": {"name": "Cooking & Food", "project_code": "COOK"},
                "project_code": "COOK",
                "video_link": "https://example.com/video3.mp4",
                "thumbnail_url": "https://example.com/thumb3.jpg"
            },
            {
                "title": "Advanced Python Programming",
                "slug": "advanced-python",
                "view_count": 300,
                "upvote_count": 45,
                "bookmark_count": 25,
                "rating_count": 15,
                "average_rating": 4.8,
                "tags": ["python", "programming", "advanced"],
                "category": {"name": "education", "id": 1},
                "topic": {"name": "Programming", "project_code": "EV"},
                "project_code": "EV",
                "video_link": "https://example.com/video4.mp4",
                "thumbnail_url": "https://example.com/thumb4.jpg"
            },
            {
                "title": "Meditation for Stress Relief",
                "slug": "meditation-stress",
                "view_count": 180,
                "upvote_count": 30,
                "bookmark_count": 12,
                "rating_count": 10,
                "average_rating": 4.3,
                "tags": ["meditation", "stress", "wellness"],
                "category": {"name": "wellness", "id": 4},
                "topic": {"name": "Mental Health", "project_code": "WELL"},
                "project_code": "WELL",
                "video_link": "https://example.com/video5.mp4",
                "thumbnail_url": "https://example.com/thumb5.jpg"
            }
        ]
        
        posts = []
        for post_data in posts_data:
            post = models.Post(**post_data)
            db.add(post)
            posts.append(post)
        
        db.commit()
        print(f"Created {len(posts)} posts")
        
        # Create sample interactions
        interactions_data = [
            # Alice likes ML and programming
            {"user_id": 1, "post_id": 1, "type": "view", "value": None},
            {"user_id": 1, "post_id": 1, "type": "like", "value": None},
            {"user_id": 1, "post_id": 4, "type": "view", "value": None},
            {"user_id": 1, "post_id": 4, "type": "bookmark", "value": None},
            {"user_id": 1, "post_id": 4, "type": "rating", "value": 5.0},
            
            # Bob likes fitness and wellness
            {"user_id": 2, "post_id": 2, "type": "view", "value": None},
            {"user_id": 2, "post_id": 2, "type": "like", "value": None},
            {"user_id": 2, "post_id": 5, "type": "view", "value": None},
            {"user_id": 2, "post_id": 5, "type": "bookmark", "value": None},
            
            # Charlie likes cooking and lifestyle
            {"user_id": 3, "post_id": 3, "type": "view", "value": None},
            {"user_id": 3, "post_id": 3, "type": "like", "value": None},
            {"user_id": 3, "post_id": 3, "type": "rating", "value": 4.0},
            
            # Diana has diverse interests
            {"user_id": 4, "post_id": 1, "type": "view", "value": None},
            {"user_id": 4, "post_id": 2, "type": "view", "value": None},
            {"user_id": 4, "post_id": 5, "type": "like", "value": None},
            
            # Eve is new (minimal interactions)
            {"user_id": 5, "post_id": 1, "type": "view", "value": None}
        ]
        
        interactions = []
        for interaction_data in interactions_data:
            interaction = models.Interaction(**interaction_data)
            db.add(interaction)
            interactions.append(interaction)
        
        db.commit()
        print(f"Created {len(interactions)} interactions")
        
        print("\nSample data created successfully!")
        print("Users:", [u.username for u in users])
        print("Posts:", [p.title for p in posts])
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    load_dotenv()
    create_sample_data()

if __name__ == "__main__":
    main()