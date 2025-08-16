#!/usr/bin/env python3
"""
Test script to verify all API endpoints are working correctly
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(url, description):
    """Test a single endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:500]}...")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    """Run all endpoint tests"""
    print("🚀 Video Recommendation Engine - Endpoint Tests")
    print("=" * 60)
    
    tests = [
        # Basic health check
        (f"{BASE_URL}/", "Health check endpoint"),
        
        # Main feed endpoint - existing users
        (f"{BASE_URL}/feed?username=alice&top_k=3", "Alice's personalized feed"),
        (f"{BASE_URL}/feed?username=bob&top_k=2", "Bob's personalized feed"),
        (f"{BASE_URL}/feed?username=charlie&top_k=2", "Charlie's personalized feed"),
        
        # Category filtering
        (f"{BASE_URL}/feed?username=alice&category=education&top_k=2", "Alice's education content"),
        (f"{BASE_URL}/feed?username=bob&category=fitness&top_k=2", "Bob's fitness content"),
        (f"{BASE_URL}/feed?username=charlie&category=lifestyle&top_k=2", "Charlie's lifestyle content"),
        
        # Project code filtering
        (f"{BASE_URL}/feed?username=alice&project_code=EV&top_k=2", "Alice's EV project content"),
        (f"{BASE_URL}/feed?username=bob&project_code=FIT&top_k=2", "Bob's FIT project content"),
        
        # Tag filtering
        (f"{BASE_URL}/feed?username=alice&tag=python&top_k=2", "Alice's Python content"),
        (f"{BASE_URL}/feed?username=bob&tag=fitness&top_k=2", "Bob's fitness tagged content"),
        (f"{BASE_URL}/feed?username=charlie&tag=cooking&top_k=2", "Charlie's cooking content"),
        
        # Combined filters
        (f"{BASE_URL}/feed?username=alice&category=education&project_code=EV&top_k=2", "Alice's EV education content"),
        
        # Cold start scenarios (new users)
        (f"{BASE_URL}/feed?username=newuser1&top_k=3", "New user - popular content"),
        (f"{BASE_URL}/feed?username=newuser2&category=fitness&top_k=2", "New user - fitness content"),
        (f"{BASE_URL}/feed?username=newuser3&project_code=EV&top_k=2", "New user - EV project content"),
        (f"{BASE_URL}/feed?username=newuser4&tag=programming&top_k=2", "New user - programming content"),
        
        # Legacy endpoint
        (f"{BASE_URL}/recommend/1?top_k=3", "Legacy endpoint - User ID 1"),
        (f"{BASE_URL}/recommend/2?top_k=2", "Legacy endpoint - User ID 2"),
        
        # Edge cases
        (f"{BASE_URL}/feed?username=alice&top_k=100", "Large top_k value"),
        (f"{BASE_URL}/feed?username=alice&top_k=1", "Small top_k value"),
        (f"{BASE_URL}/feed?username=nonexistent&category=nonexistent&top_k=2", "Non-existent user and category"),
    ]
    
    passed = 0
    total = len(tests)
    
    for url, description in tests:
        if test_endpoint(url, description):
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the issues above.")
    
    print("\n🔗 API Documentation available at:")
    print(f"   - Swagger UI: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    main()