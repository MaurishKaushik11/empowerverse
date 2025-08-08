#!/usr/bin/env python3
"""
EmpowerVerse Demo Startup Script
Starts the server on 127.0.0.1:8000 for presentation
"""

import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("🚀 Starting EmpowerVerse Demo Server...")
    print("=" * 50)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print(f"📁 Working directory: {project_dir}")
    print("🌐 Server will be available at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("📊 Demo Dashboard: http://127.0.0.1:8000/api/v1/demo/dashboard")
    print()
    
    # Ask if user wants to open browser
    try:
        open_browser = input("🌐 Open browser automatically? (y/n): ").lower().strip()
        if open_browser in ['y', 'yes', '']:
            print("⏳ Will open browser in 3 seconds after server starts...")
            auto_open = True
        else:
            auto_open = False
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        return
    
    print("\n🔄 Starting Uvicorn server...")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the server
        if auto_open:
            # Start server in background and open browser
            import threading
            
            def open_browser_delayed():
                time.sleep(3)
                try:
                    webbrowser.open("http://127.0.0.1:8000/docs")
                    print("\n🌐 Opened browser with API documentation")
                except Exception as e:
                    print(f"\n⚠️ Could not open browser: {e}")
            
            browser_thread = threading.Thread(target=open_browser_delayed)
            browser_thread.daemon = True
            browser_thread.start()
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("✅ EmpowerVerse demo session ended")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("💡 Make sure you're in the project directory and have all dependencies installed")

if __name__ == "__main__":
    main()