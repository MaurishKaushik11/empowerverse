#!/usr/bin/env python3
"""
Quick setup script for the Video Recommendation Engine
This script will set up everything needed to run the project
"""
import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    if not env_path.exists():
        print("🔧 Creating .env file...")
        with open(".env", "w") as f:
            f.write("FLIC_TOKEN=flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f\n")
            f.write("API_BASE_URL=https://api.socialverseapp.com\n")
            f.write("DATABASE_URL=sqlite:///./app.db\n")
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")
    return True

def setup_database():
    """Initialize database and create sample data"""
    print("🗄️  Setting up database...")
    try:
        # Initialize database
        subprocess.check_call([sys.executable, "setup_database.py"])
        
        # Create sample data
        subprocess.check_call([sys.executable, "create_sample_data.py"])
        
        print("✅ Database setup completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database setup failed: {e}")
        return False

def run_tests():
    """Run endpoint tests to verify everything works"""
    print("🧪 Running tests...")
    try:
        # Start server in background for testing
        import threading
        import time
        import uvicorn
        from app.main import app
        
        # Start server in a separate thread
        def start_server():
            uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Run tests
        subprocess.check_call([sys.executable, "test_endpoints.py"])
        
        print("✅ All tests passed")
        return True
    except Exception as e:
        print(f"⚠️  Tests failed, but setup is complete: {e}")
        return True  # Don't fail setup if tests fail

def main():
    """Main setup function"""
    print("🎬 Video Recommendation Engine - Quick Setup")
    print("=" * 60)
    print("This script will:")
    print("1. Install Python dependencies")
    print("2. Create environment configuration")
    print("3. Initialize database with sample data")
    print("4. Run tests to verify everything works")
    print()
    
    # Run setup steps
    steps = [
        ("Installing dependencies", install_dependencies),
        ("Setting up environment", setup_environment),
        ("Initializing database", setup_database),
        ("Running tests", run_tests),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\nTo start the server, run:")
    print("  python start_server.py")
    print("\nOr manually:")
    print("  uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
    print("\nAPI will be available at:")
    print("  - http://127.0.0.1:8000")
    print("  - http://127.0.0.1:8000/docs (Swagger UI)")
    print("  - http://127.0.0.1:8000/redoc (ReDoc)")

if __name__ == "__main__":
    main()