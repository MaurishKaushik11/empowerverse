#!/usr/bin/env python3
"""
Demo Setup Script for EmpowerVerse
Sets up sample data and provides instructions for presentation
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr}")
        return False

def main():
    print("🚀 EmpowerVerse Demo Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app"):
        print("❌ Please run this script from the project directory")
        print("   Expected structure: project/app/")
        return
    
    print("📊 Setting up sample database...")
    
    # Create sample data
    if run_command("python create_sample_data.py", "Creating sample data"):
        print("\n🎉 Sample data created successfully!")
        
        print("\n📋 Demo Endpoints Available:")
        print("   • http://localhost:8000/docs - Interactive API documentation")
        print("   • http://localhost:8000/api/v1/demo/dashboard - Dashboard statistics")
        print("   • http://localhost:8000/api/v1/demo/users - Sample users")
        print("   • http://localhost:8000/api/v1/demo/posts - Sample posts with videos")
        print("   • http://localhost:8000/api/v1/demo/categories - Content categories")
        print("   • http://localhost:8000/api/v1/demo/interactions/stats - User engagement stats")
        
        print("\n🎯 Presentation-Ready Features:")
        print("   ✅ 5 diverse user profiles with different interests")
        print("   ✅ 8 engaging posts with real YouTube video content")
        print("   ✅ 6 content categories (Tech, Business, Personal Dev, etc.)")
        print("   ✅ 4 discussion topics with community engagement")
        print("   ✅ Realistic user interactions (views, likes, bookmarks)")
        print("   ✅ ML embeddings for recommendation algorithms")
        print("   ✅ Recommendation logs showing AI decision-making")
        
        print("\n🚀 To start the demo server:")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        
        print("\n💡 Demo Scenarios for Presentation:")
        print("   1. Show user profiles: GET /api/v1/demo/users")
        print("   2. Display engaging content: GET /api/v1/demo/posts")
        print("   3. Demonstrate categories: GET /api/v1/demo/categories")
        print("   4. Show engagement metrics: GET /api/v1/demo/interactions/stats")
        print("   5. Display dashboard overview: GET /api/v1/demo/dashboard")
        print("   6. Show personalized recommendations: GET /api/v1/feed?username=alex_entrepreneur")
        
        print("\n🎬 Sample Users for Demo:")
        print("   • alex_entrepreneur - Business & startup focused")
        print("   • sarah_developer - Tech & programming enthusiast")
        print("   • mike_student - Learning & career development")
        print("   • emma_creator - Creative & marketing content")
        print("   • david_investor - Finance & crypto investing")
        
        print("\n📱 Frontend Integration:")
        print("   The API provides all data needed for a React frontend")
        print("   Each post includes thumbnail URLs for video previews")
        print("   User profiles include profile pictures and preferences")
        print("   Categories have cover images for visual appeal")
        
        print("\n🔥 Ready for presentation! Your EmpowerVerse demo is fully loaded.")
        
    else:
        print("\n❌ Failed to create sample data. Please check the error messages above.")

if __name__ == "__main__":
    main()