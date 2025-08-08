#!/usr/bin/env python3
"""
Check PostgreSQL database content directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL from config
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/video_recommendation_db"
engine = create_engine(DATABASE_URL, echo=False)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def check_database():
    try:
        # Check users table
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        print(f"Users in database: {user_count}")
        
        if user_count > 0:
            result = db.execute(text("SELECT username, first_name, last_name, user_type FROM users LIMIT 5"))
            users = result.fetchall()
            print("Sample users:")
            for user in users:
                print(f"  - {user[1]} {user[2]} (@{user[0]}) - {user[3]}")
        
        # Check posts table
        result = db.execute(text("SELECT COUNT(*) FROM posts"))
        post_count = result.scalar()
        print(f"\nPosts in database: {post_count}")
        
        if post_count > 0:
            result = db.execute(text("SELECT title, view_count, upvote_count FROM posts LIMIT 5"))
            posts = result.fetchall()
            print("Sample posts:")
            for post in posts:
                print(f"  - \"{post[0]}\" - {post[1]} views, {post[2]} upvotes")
        
        # Check categories table
        result = db.execute(text("SELECT COUNT(*) FROM categories"))
        category_count = result.scalar()
        print(f"\nCategories in database: {category_count}")
        
        if category_count > 0:
            result = db.execute(text("SELECT name, description FROM categories LIMIT 5"))
            categories = result.fetchall()
            print("Sample categories:")
            for cat in categories:
                print(f"  - {cat[0]}: {cat[1]}")
        
        # Check interactions
        result = db.execute(text("SELECT COUNT(*) FROM user_interactions"))
        interaction_count = result.scalar()
        print(f"\nInteractions in database: {interaction_count}")
        
    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database()