#!/usr/bin/env python3
"""
Setup script to initialize the database and collect initial data
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from dotenv import load_dotenv
from app.database.database import engine, Base
from app.database import models

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def collect_data():
    """Collect data from API"""
    print("\n=== Collecting Users ===")
    try:
        from app.collect_users import save_users
        save_users()
    except Exception as e:
        print(f"Error collecting users: {e}")
    
    print("\n=== Collecting Posts ===")
    try:
        from app.collect_data import save_posts
        save_posts()
    except Exception as e:
        print(f"Error collecting posts: {e}")
    
    print("\n=== Collecting Interactions ===")
    try:
        from app.collect_interactions import save_interactions_from_api, save_interactions_synthetic
        real_saved = save_interactions_from_api()
        if real_saved == 0:
            print("No real interactions found, generating synthetic ones...")
            save_interactions_synthetic()
    except Exception as e:
        print(f"Error collecting interactions: {e}")

def main():
    """Main setup function"""
    load_dotenv()
    
    print("=== Video Recommendation Engine Setup ===")
    print("This script will:")
    print("1. Create database tables")
    print("2. Collect users from API")
    print("3. Collect posts from API")
    print("4. Generate interactions")
    print()
    
    # Create tables
    create_tables()
    
    # Collect data
    collect_data()
    
    print("\n=== Setup Complete! ===")
    print("You can now start the server with:")
    print("uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()