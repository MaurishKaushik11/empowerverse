#!/usr/bin/env python3
"""
Development startup script for EmpowerVerse Video Recommendation Engine
"""

import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import torch
        import tensorflow
        logger.info("All major dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.info("Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables and directories"""
    # Create necessary directories
    directories = ['models', 'logs', 'data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Created/verified directory: {directory}")
    
    # Check for .env file
    if not Path('.env').exists():
        logger.warning(".env file not found. Using default configuration.")
        logger.info("Consider copying .env.example to .env and updating values")
    
    return True

def run_database_migrations():
    """Run database migrations"""
    try:
        logger.info("Running database migrations...")
        from app.database.database import init_db
        init_db()
        logger.info("Database migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    logger.info("Starting FastAPI backend server...")
    try:
        cmd = [
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ]
        
        process = subprocess.Popen(cmd)
        logger.info("Backend server started on http://localhost:8000")
        logger.info("API documentation available at http://localhost:8000/docs")
        return process
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        return None

def start_frontend():
    """Start the React frontend development server"""
    logger.info("Starting React frontend development server...")
    try:
        # Check if node_modules exists
        if not Path('node_modules').exists():
            logger.info("Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        cmd = ['npm', 'run', 'dev']
        process = subprocess.Popen(cmd)
        logger.info("Frontend server started on http://localhost:5173")
        return process
    except Exception as e:
        logger.error(f"Failed to start frontend server: {e}")
        return None

def main():
    """Main startup function"""
    logger.info("🚀 Starting EmpowerVerse Development Environment")
    
    # Pre-flight checks
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not setup_environment():
        sys.exit(1)
    
    if not run_database_migrations():
        logger.warning("Database migrations failed, but continuing...")
    
    # Start services
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    frontend_process = start_frontend()
    if not frontend_process:
        logger.warning("Frontend server failed to start")
    
    logger.info("✅ Development environment is ready!")
    logger.info("Backend API: http://localhost:8000")
    logger.info("Frontend App: http://localhost:5173")
    logger.info("API Docs: http://localhost:8000/docs")
    logger.info("\nPress Ctrl+C to stop all servers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down development environment...")
        
        if backend_process:
            backend_process.terminate()
            logger.info("Backend server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            logger.info("Frontend server stopped")
        
        logger.info("Development environment stopped")

if __name__ == "__main__":
    main()