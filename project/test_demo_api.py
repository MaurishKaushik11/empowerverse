#!/usr/bin/env python3
"""
Test script for EmpowerVerse Demo API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, description):
    """Test an API endpoint and display results"""
    print(f"\n🔍 Testing: {description}")
    print(f"   Endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Status: {response.status_code}")
            
            # Display key information based on endpoint
            if "users" in endpoint:
                print(f"   📊 Found {data.get('total_users', 0)} users")
                if data.get('users'):
                    for user in data['users'][:2]:  # Show first 2 users
                        print(f"      • {user['first_name']} {user['last_name']} (@{user['username']}) - {user['user_type']}")
            
            elif "posts" in endpoint:
                print(f"   📊 Found {data.get('total_posts', 0)} posts")
                if data.get('posts'):
                    for post in data['posts'][:2]:  # Show first 2 posts
                        print(f"      • \"{post['title']}\" - {post['view_count']} views, {post['upvote_count']} upvotes")
            
            elif "categories" in endpoint:
                print(f"   📊 Found {data.get('total_categories', 0)} categories")
                if data.get('categories'):
                    for cat in data['categories'][:3]:  # Show first 3 categories
                        print(f"      • {cat['name']} - {cat['post_count']} posts, {cat['total_views']} total views")
            
            elif "dashboard" in endpoint:
                overview = data.get('overview', {})
                engagement = data.get('engagement', {})
                print(f"   📊 Dashboard Overview:")
                print(f"      • Users: {overview.get('total_users', 0)}")
                print(f"      • Posts: {overview.get('total_posts', 0)}")
                print(f"      • Total Views: {engagement.get('total_views', 0):,}")
                print(f"      • Average Rating: {engagement.get('average_rating', 0)}/5.0")
            
            elif "interactions/stats" in endpoint:
                print(f"   📊 Interaction Statistics:")
                print(f"      • Total Interactions: {data.get('total_interactions', 0)}")
                interaction_types = data.get('interaction_types', [])
                for interaction in interaction_types[:3]:
                    print(f"      • {interaction['type']}: {interaction['count']} times")
            
            return True
        else:
            print(f"   ❌ Failed! Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Server not running on {BASE_URL}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Test all demo endpoints"""
    print("🚀 EmpowerVerse Demo API Test")
    print("=" * 50)
    
    # Test basic server health
    print(f"\n🏥 Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"   ✅ Server is healthy!")
        else:
            print(f"   ⚠️ Server health check failed")
    except:
        print(f"   ❌ Cannot connect to server at {BASE_URL}")
        print(f"   💡 Make sure the server is running with:")
        print(f"      python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Test demo endpoints
    endpoints = [
        ("/api/v1/demo/users", "Sample Users"),
        ("/api/v1/demo/posts", "Sample Posts"),
        ("/api/v1/demo/categories", "Content Categories"),
        ("/api/v1/demo/topics", "Discussion Topics"),
        ("/api/v1/demo/interactions/stats", "User Interaction Statistics"),
        ("/api/v1/demo/dashboard", "Dashboard Overview"),
        ("/api/v1/demo/user/alex_entrepreneur/profile", "User Profile Example")
    ]
    
    successful_tests = 0
    total_tests = len(endpoints)
    
    for endpoint, description in endpoints:
        if test_endpoint(endpoint, description):
            successful_tests += 1
    
    print(f"\n📊 Test Results:")
    print(f"   ✅ Successful: {successful_tests}/{total_tests}")
    print(f"   ❌ Failed: {total_tests - successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print(f"\n🎉 All tests passed! Your EmpowerVerse demo API is ready!")
        print(f"\n🌐 Access your API documentation at:")
        print(f"   • Interactive Docs: {BASE_URL}/docs")
        print(f"   • ReDoc: {BASE_URL}/redoc")
        
        print(f"\n🎯 Demo URLs for Presentation:")
        print(f"   • Dashboard: {BASE_URL}/api/v1/demo/dashboard")
        print(f"   • Users: {BASE_URL}/api/v1/demo/users")
        print(f"   • Posts: {BASE_URL}/api/v1/demo/posts")
        print(f"   • Categories: {BASE_URL}/api/v1/demo/categories")
        print(f"   • User Interactions: {BASE_URL}/api/v1/demo/interactions/stats")
    else:
        print(f"\n⚠️ Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()