#!/usr/bin/env python3
"""
Simple startup script for the Video Recommendation Engine
"""
import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_database():
    """Check if database exists and has data"""
    db_path = Path("app.db")
    if not db_path.exists():
        print("❌ Database not found")
        print("Please run: python setup_database.py && python create_sample_data.py")
        return False
    
    # Check if database has data
    try:
        import sqlite3
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        # Check if tables exist and have data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM posts")
        post_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM interactions")
        interaction_count = cursor.fetchone()[0]
        
        conn.close()
        
        if user_count == 0 or post_count == 0:
            print("❌ Database is empty")
            print("Please run: python create_sample_data.py")
            return False
        
        print(f"✅ Database ready: {user_count} users, {post_count} posts, {interaction_count} interactions")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_env():
    """Check if .env file exists"""
    env_path = Path(".env")
    if not env_path.exists():
        print("⚠️  .env file not found, creating default...")
        with open(".env", "w") as f:
            f.write("FLIC_TOKEN=flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f\n")
            f.write("API_BASE_URL=https://api.socialverseapp.com\n")
            f.write("DATABASE_URL=sqlite:///./app.db\n")
        print("✅ Created default .env file")
    else:
        print("✅ .env file found")
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Video Recommendation Engine...")
    print("Server will be available at:")
    print("  - API: http://127.0.0.1:8000")
    print("  - Swagger UI: http://127.0.0.1:8000/docs")
    print("  - ReDoc: http://127.0.0.1:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    """Main startup function"""
    print("🎬 Video Recommendation Engine - Startup Check")
    print("=" * 50)
    
    # Check all prerequisites
    if not check_env():
        return
    
    if not check_dependencies():
        return
    
    if not check_database():
        return
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()