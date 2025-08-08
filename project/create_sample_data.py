#!/usr/bin/env python3
"""
Sample Data Generator for EmpowerVerse
Creates realistic sample data for presentation and demo purposes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from app.database.database import engine, Base
from app.database.models import (
    User, Post, Category, Topic, UserInteraction, 
    UserEmbedding, PostEmbedding, RecommendationLog
)
from datetime import datetime, timedelta
import random
import json

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_sample_users():
    """Create diverse sample users"""
    users_data = [
        {
            "username": "alex_entrepreneur",
            "first_name": "Alex",
            "last_name": "Johnson",
            "email": "alex.johnson@example.com",
            "picture_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
            "user_type": "entrepreneur",
            "has_evm_wallet": True,
            "has_solana_wallet": False,
            "preferences": {
                "interests": ["business", "technology", "startups"],
                "content_types": ["educational", "motivational"],
                "difficulty_level": "intermediate"
            }
        },
        {
            "username": "sarah_developer",
            "first_name": "Sarah",
            "last_name": "Chen",
            "email": "sarah.chen@example.com",
            "picture_url": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
            "user_type": "developer",
            "has_evm_wallet": True,
            "has_solana_wallet": True,
            "preferences": {
                "interests": ["programming", "web3", "ai"],
                "content_types": ["tutorials", "technical"],
                "difficulty_level": "advanced"
            }
        },
        {
            "username": "mike_student",
            "first_name": "Mike",
            "last_name": "Rodriguez",
            "email": "mike.rodriguez@example.com",
            "picture_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
            "user_type": "student",
            "has_evm_wallet": False,
            "has_solana_wallet": False,
            "preferences": {
                "interests": ["learning", "career", "skills"],
                "content_types": ["educational", "beginner-friendly"],
                "difficulty_level": "beginner"
            }
        },
        {
            "username": "emma_creator",
            "first_name": "Emma",
            "last_name": "Wilson",
            "email": "emma.wilson@example.com",
            "picture_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
            "user_type": "content_creator",
            "has_evm_wallet": True,
            "has_solana_wallet": False,
            "preferences": {
                "interests": ["creativity", "marketing", "social_media"],
                "content_types": ["creative", "inspirational"],
                "difficulty_level": "intermediate"
            }
        },
        {
            "username": "david_investor",
            "first_name": "David",
            "last_name": "Kim",
            "email": "david.kim@example.com",
            "picture_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
            "user_type": "investor",
            "has_evm_wallet": True,
            "has_solana_wallet": True,
            "preferences": {
                "interests": ["finance", "crypto", "investing"],
                "content_types": ["analysis", "market_insights"],
                "difficulty_level": "advanced"
            }
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)
    
    db.commit()
    return users

def create_categories():
    """Create content categories"""
    categories_data = [
        {
            "name": "Technology",
            "description": "Latest in tech, programming, AI, and digital innovation",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=300&h=200&fit=crop",
            "count": 0
        },
        {
            "name": "Business & Entrepreneurship",
            "description": "Startup advice, business strategies, and entrepreneurial insights",
            "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=300&h=200&fit=crop",
            "count": 0
        },
        {
            "name": "Personal Development",
            "description": "Self-improvement, productivity, and life skills",
            "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=300&h=200&fit=crop",
            "count": 0
        },
        {
            "name": "Finance & Investing",
            "description": "Financial literacy, investing strategies, and market analysis",
            "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=300&h=200&fit=crop",
            "count": 0
        },
        {
            "name": "Health & Wellness",
            "description": "Mental health, fitness, and overall well-being",
            "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=200&fit=crop",
            "count": 0
        },
        {
            "name": "Creative Arts",
            "description": "Design, creativity, and artistic expression",
            "image_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=300&h=200&fit=crop",
            "count": 0
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        categories.append(category)
    
    db.commit()
    return categories

def create_topics(users):
    """Create discussion topics"""
    topics_data = [
        {
            "name": "AI & Machine Learning",
            "description": "Exploring artificial intelligence and machine learning concepts",
            "slug": "ai-machine-learning",
            "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=300&h=200&fit=crop",
            "is_public": True,
            "project_code": "AI_ML_2024",
            "posts_count": 0,
            "language": "English",
            "owner_id": users[1].id  # Sarah (developer)
        },
        {
            "name": "Startup Success Stories",
            "description": "Real stories from successful entrepreneurs and startups",
            "slug": "startup-success-stories",
            "image_url": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=300&h=200&fit=crop",
            "is_public": True,
            "project_code": "STARTUP_2024",
            "posts_count": 0,
            "language": "English",
            "owner_id": users[0].id  # Alex (entrepreneur)
        },
        {
            "name": "Web3 & Blockchain",
            "description": "Decentralized technologies and blockchain development",
            "slug": "web3-blockchain",
            "image_url": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=300&h=200&fit=crop",
            "is_public": True,
            "project_code": "WEB3_2024",
            "posts_count": 0,
            "language": "English",
            "owner_id": users[4].id  # David (investor)
        },
        {
            "name": "Productivity Hacks",
            "description": "Tips and tricks to boost your productivity",
            "slug": "productivity-hacks",
            "image_url": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=300&h=200&fit=crop",
            "is_public": True,
            "project_code": "PROD_2024",
            "posts_count": 0,
            "language": "English",
            "owner_id": users[3].id  # Emma (creator)
        }
    ]
    
    topics = []
    for topic_data in topics_data:
        topic = Topic(**topic_data)
        db.add(topic)
        topics.append(topic)
    
    db.commit()
    return topics

def create_sample_posts(users, categories, topics):
    """Create engaging sample posts with real video content"""
    posts_data = [
        {
            "title": "The Future of AI: What Every Developer Should Know",
            "slug": "future-of-ai-developers",
            "owner_id": users[1].id,  # Sarah
            "category_id": categories[0].id,  # Technology
            "topic_id": topics[0].id,  # AI & ML
            "video_link": "https://www.youtube.com/watch?v=JMLsJJuOwDE",
            "thumbnail_url": "https://img.youtube.com/vi/JMLsJJuOwDE/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/JMLsJJuOwDE/hqdefault.jpg",
            "view_count": 15420,
            "upvote_count": 892,
            "comment_count": 156,
            "share_count": 234,
            "bookmark_count": 445,
            "rating_count": 234,
            "average_rating": 4.7,
            "tags": ["AI", "Machine Learning", "Programming", "Future Tech"]
        },
        {
            "title": "From Zero to Startup: My Journey Building a $1M Company",
            "slug": "zero-to-startup-journey",
            "owner_id": users[0].id,  # Alex
            "category_id": categories[1].id,  # Business
            "topic_id": topics[1].id,  # Startup Stories
            "video_link": "https://www.youtube.com/watch?v=ZoqgAy3h4OM",
            "thumbnail_url": "https://img.youtube.com/vi/ZoqgAy3h4OM/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/ZoqgAy3h4OM/hqdefault.jpg",
            "view_count": 28750,
            "upvote_count": 1456,
            "comment_count": 289,
            "share_count": 567,
            "bookmark_count": 789,
            "rating_count": 445,
            "average_rating": 4.8,
            "tags": ["Startup", "Entrepreneurship", "Business", "Success Story"]
        },
        {
            "title": "Web3 Development: Building Your First DApp",
            "slug": "web3-development-first-dapp",
            "owner_id": users[1].id,  # Sarah
            "category_id": categories[0].id,  # Technology
            "topic_id": topics[2].id,  # Web3
            "video_link": "https://www.youtube.com/watch?v=M576WGiDBdQ",
            "thumbnail_url": "https://img.youtube.com/vi/M576WGiDBdQ/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/M576WGiDBdQ/hqdefault.jpg",
            "view_count": 12340,
            "upvote_count": 678,
            "comment_count": 123,
            "share_count": 189,
            "bookmark_count": 334,
            "rating_count": 189,
            "average_rating": 4.6,
            "tags": ["Web3", "Blockchain", "DApp", "Smart Contracts"]
        },
        {
            "title": "10 Productivity Hacks That Changed My Life",
            "slug": "10-productivity-hacks-life-changing",
            "owner_id": users[3].id,  # Emma
            "category_id": categories[2].id,  # Personal Development
            "topic_id": topics[3].id,  # Productivity
            "video_link": "https://www.youtube.com/watch?v=1LAkuiJ0QsU",
            "thumbnail_url": "https://img.youtube.com/vi/1LAkuiJ0QsU/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/1LAkuiJ0QsU/hqdefault.jpg",
            "view_count": 45670,
            "upvote_count": 2134,
            "comment_count": 456,
            "share_count": 789,
            "bookmark_count": 1234,
            "rating_count": 567,
            "average_rating": 4.9,
            "tags": ["Productivity", "Life Hacks", "Time Management", "Efficiency"]
        },
        {
            "title": "Cryptocurrency Investment Strategy for Beginners",
            "slug": "crypto-investment-strategy-beginners",
            "owner_id": users[4].id,  # David
            "category_id": categories[3].id,  # Finance
            "topic_id": topics[2].id,  # Web3
            "video_link": "https://www.youtube.com/watch?v=VYWc9dFqROI",
            "thumbnail_url": "https://img.youtube.com/vi/VYWc9dFqROI/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/VYWc9dFqROI/hqdefault.jpg",
            "view_count": 34560,
            "upvote_count": 1789,
            "comment_count": 345,
            "share_count": 456,
            "bookmark_count": 678,
            "rating_count": 389,
            "average_rating": 4.5,
            "tags": ["Cryptocurrency", "Investment", "Finance", "Beginner Guide"]
        },
        {
            "title": "The Psychology of Success: Mindset Matters",
            "slug": "psychology-success-mindset-matters",
            "owner_id": users[2].id,  # Mike
            "category_id": categories[2].id,  # Personal Development
            "topic_id": topics[1].id,  # Startup Stories
            "video_link": "https://www.youtube.com/watch?v=H14bBuluwB8",
            "thumbnail_url": "https://img.youtube.com/vi/H14bBuluwB8/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/H14bBuluwB8/hqdefault.jpg",
            "view_count": 23450,
            "upvote_count": 1123,
            "comment_count": 234,
            "share_count": 345,
            "bookmark_count": 567,
            "rating_count": 278,
            "average_rating": 4.7,
            "tags": ["Psychology", "Success", "Mindset", "Personal Growth"]
        },
        {
            "title": "Creative Design Principles Every Entrepreneur Should Know",
            "slug": "creative-design-principles-entrepreneurs",
            "owner_id": users[3].id,  # Emma
            "category_id": categories[5].id,  # Creative Arts
            "topic_id": topics[1].id,  # Startup Stories
            "video_link": "https://www.youtube.com/watch?v=a5KYlHNKQB8",
            "thumbnail_url": "https://img.youtube.com/vi/a5KYlHNKQB8/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/a5KYlHNKQB8/hqdefault.jpg",
            "view_count": 18920,
            "upvote_count": 945,
            "comment_count": 178,
            "share_count": 267,
            "bookmark_count": 423,
            "rating_count": 201,
            "average_rating": 4.6,
            "tags": ["Design", "Creativity", "Entrepreneurship", "Visual Communication"]
        },
        {
            "title": "Mental Health in Tech: Managing Burnout and Stress",
            "slug": "mental-health-tech-burnout-stress",
            "owner_id": users[1].id,  # Sarah
            "category_id": categories[4].id,  # Health & Wellness
            "topic_id": topics[3].id,  # Productivity
            "video_link": "https://www.youtube.com/watch?v=tFMqmZt3v_s",
            "thumbnail_url": "https://img.youtube.com/vi/tFMqmZt3v_s/maxresdefault.jpg",
            "gif_thumbnail_url": "https://img.youtube.com/vi/tFMqmZt3v_s/hqdefault.jpg",
            "view_count": 31240,
            "upvote_count": 1567,
            "comment_count": 298,
            "share_count": 445,
            "bookmark_count": 789,
            "rating_count": 334,
            "average_rating": 4.8,
            "tags": ["Mental Health", "Tech Industry", "Burnout", "Wellness"]
        }
    ]
    
    posts = []
    for post_data in posts_data:
        # Add some randomness to creation dates (last 30 days)
        days_ago = random.randint(1, 30)
        post_data['created_at'] = datetime.utcnow() - timedelta(days=days_ago)
        post_data['updated_at'] = post_data['created_at']
        
        post = Post(**post_data)
        db.add(post)
        posts.append(post)
    
    db.commit()
    return posts

def create_user_interactions(users, posts):
    """Create realistic user interactions"""
    interaction_types = ['view', 'like', 'bookmark', 'share', 'rate']
    
    interactions = []
    for user in users:
        # Each user interacts with 60-80% of posts
        user_posts = random.sample(posts, random.randint(int(len(posts) * 0.6), int(len(posts) * 0.8)))
        
        for post in user_posts:
            # Multiple interactions per post
            num_interactions = random.randint(1, 3)
            user_interaction_types = random.sample(interaction_types, num_interactions)
            
            for interaction_type in user_interaction_types:
                interaction_value = None
                if interaction_type == 'rate':
                    interaction_value = random.uniform(3.5, 5.0)  # Rating between 3.5-5.0
                elif interaction_type == 'view':
                    interaction_value = random.uniform(30, 600)  # Watch time in seconds
                
                # Random timestamp within last 30 days
                days_ago = random.randint(1, 30)
                timestamp = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
                
                interaction = UserInteraction(
                    user_id=user.id,
                    post_id=post.id,
                    interaction_type=interaction_type,
                    interaction_value=interaction_value,
                    timestamp=timestamp
                )
                db.add(interaction)
                interactions.append(interaction)
    
    db.commit()
    return interactions

def create_embeddings(users, posts):
    """Create sample embeddings for ML recommendations"""
    user_embeddings = []
    post_embeddings = []
    
    # Create user embeddings (384-dimensional vectors for demo)
    for user in users:
        embedding_vector = [random.uniform(-1, 1) for _ in range(384)]
        user_embedding = UserEmbedding(
            user_id=user.id,
            embedding_vector=embedding_vector,
            model_version="sentence-transformers/all-MiniLM-L6-v2"
        )
        db.add(user_embedding)
        user_embeddings.append(user_embedding)
    
    # Create post embeddings
    for post in posts:
        content_embedding = [random.uniform(-1, 1) for _ in range(384)]
        engagement_embedding = [random.uniform(-1, 1) for _ in range(128)]
        
        post_embedding = PostEmbedding(
            post_id=post.id,
            content_embedding=content_embedding,
            engagement_embedding=engagement_embedding,
            model_version="hybrid-v1.0"
        )
        db.add(post_embedding)
        post_embeddings.append(post_embedding)
    
    db.commit()
    return user_embeddings, post_embeddings

def create_recommendation_logs(users, posts):
    """Create sample recommendation logs"""
    algorithms = ["collaborative_filtering", "content_based", "hybrid", "neural_network"]
    
    logs = []
    for user in users:
        # Create 3-5 recommendation logs per user
        for _ in range(random.randint(3, 5)):
            # Recommend 5-10 posts
            recommended_posts = random.sample([p.id for p in posts], random.randint(5, 10))
            confidence_scores = [random.uniform(0.6, 0.95) for _ in recommended_posts]
            
            days_ago = random.randint(1, 7)
            timestamp = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
            
            log = RecommendationLog(
                user_id=user.id,
                recommended_posts=recommended_posts,
                algorithm_used=random.choice(algorithms),
                confidence_scores=confidence_scores,
                timestamp=timestamp
            )
            db.add(log)
            logs.append(log)
    
    db.commit()
    return logs

def update_counts(categories, topics, posts):
    """Update count fields based on created data"""
    # Update category counts
    for category in categories:
        category.count = len([p for p in posts if p.category_id == category.id])
    
    # Update topic post counts
    for topic in topics:
        topic.posts_count = len([p for p in posts if p.topic_id == topic.id])
    
    db.commit()

def main():
    """Main function to create all sample data"""
    print("🚀 Creating sample data for EmpowerVerse...")
    
    try:
        # Create tables first
        print("🏗️ Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("   ✅ Database tables created")
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("📝 Clearing existing data...")
        try:
            db.query(RecommendationLog).delete()
            db.query(PostEmbedding).delete()
            db.query(UserEmbedding).delete()
            db.query(UserInteraction).delete()
            db.query(Post).delete()
            db.query(Topic).delete()
            db.query(Category).delete()
            db.query(User).delete()
            db.commit()
            print("   ✅ Existing data cleared")
        except Exception as e:
            print(f"   ⚠️ Warning: Could not clear existing data: {e}")
            db.rollback()
        
        print("👥 Creating users...")
        users = create_sample_users()
        print(f"   ✅ Created {len(users)} users")
        
        print("📂 Creating categories...")
        categories = create_categories()
        print(f"   ✅ Created {len(categories)} categories")
        
        print("💬 Creating topics...")
        topics = create_topics(users)
        print(f"   ✅ Created {len(topics)} topics")
        
        print("📹 Creating posts...")
        posts = create_sample_posts(users, categories, topics)
        print(f"   ✅ Created {len(posts)} posts")
        
        print("👆 Creating user interactions...")
        interactions = create_user_interactions(users, posts)
        print(f"   ✅ Created {len(interactions)} interactions")
        
        print("🧠 Creating embeddings...")
        user_embeddings, post_embeddings = create_embeddings(users, posts)
        print(f"   ✅ Created {len(user_embeddings)} user embeddings and {len(post_embeddings)} post embeddings")
        
        print("📊 Creating recommendation logs...")
        logs = create_recommendation_logs(users, posts)
        print(f"   ✅ Created {len(logs)} recommendation logs")
        
        print("🔢 Updating counts...")
        update_counts(categories, topics, posts)
        print("   ✅ Updated all counts")
        
        print("\n🎉 Sample data creation completed successfully!")
        print("\n📊 Summary:")
        print(f"   • {len(users)} Users with diverse profiles")
        print(f"   • {len(categories)} Content categories")
        print(f"   • {len(topics)} Discussion topics")
        print(f"   • {len(posts)} Posts with real video content")
        print(f"   • {len(interactions)} User interactions")
        print(f"   • {len(user_embeddings + post_embeddings)} ML embeddings")
        print(f"   • {len(logs)} Recommendation logs")
        print("\n🚀 Your EmpowerVerse database is now ready for presentation!")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()