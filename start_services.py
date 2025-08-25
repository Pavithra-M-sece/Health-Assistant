#!/usr/bin/env python3
"""
Healthcare App Service Manager
Starts all services (MongoDB, Backend, Frontend, AI Service) using Python
Now includes setup for new laptops: checks and installs dependencies.
"""

import os
import sys
import time
import subprocess
import threading
import signal
from pathlib import Path
import shutil
import webbrowser

class ServiceManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.processes = []
        self.running = True
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        print("\n🛑 Shutting down all services...")
        self.running = False
        self.stop_all_services()
        sys.exit(0)

    def check_and_install_dependencies(self):
        print("\n🔍 Checking system dependencies...")
        # Check Node.js
        node = shutil.which("node")
        npm = shutil.which("npm")
        if not node or not npm:
            print("❌ Node.js and/or npm are not installed or not in your PATH.")
            print("Please install Node.js (which includes npm) from: https://nodejs.org/")
            webbrowser.open("https://nodejs.org/")
            input("Press Enter after installing Node.js and npm, then re-run this script...")
            sys.exit(1)
        else:
            print(f"✅ Node.js found: {node}")
            print(f"✅ npm found: {npm}")
        # Check MongoDB
        mongod = shutil.which("mongod")
        if not mongod:
            print("❌ MongoDB is not installed or not in your PATH.")
            print("Please install MongoDB Community Edition from: https://www.mongodb.com/try/download/community")
            webbrowser.open("https://www.mongodb.com/try/download/community")
            input("Press Enter after installing MongoDB, then re-run this script...")
            sys.exit(1)
        else:
            print(f"✅ MongoDB found: {mongod}")
        # Check Python packages for AI service
        ai_dir = self.project_root / "ai_service"
        venv_dir = ai_dir / "venv"
        venv_python = venv_dir / "Scripts" / "python.exe" if os.name == 'nt' else venv_dir / "bin" / "python"
        if not venv_python.exists():
            print("⚙️  Creating Python virtual environment for AI service...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=ai_dir, check=True)
            print("✅ Virtual environment created.")
        print("⚙️  Installing Python dependencies for AI service...")
        subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], cwd=ai_dir, check=True)
        subprocess.run([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"], cwd=ai_dir, check=True)
        print("✅ Python dependencies installed.")
        # Install Node dependencies for backend and frontend
        print("⚙️  Installing backend dependencies...")
        subprocess.run([npm, "install"], cwd=self.project_root / "server", check=True)
        print("✅ Backend dependencies installed.")
        print("⚙️  Installing frontend dependencies...")
        subprocess.run([npm, "install"], cwd=self.project_root / "client", check=True)
        print("✅ Frontend dependencies installed.")
        print("\n✅ All dependencies are installed and up to date!")

    def create_mongodb_data_dir(self):
        """Create MongoDB data directory if it doesn't exist"""
        data_dir = self.project_root / "data" / "db"
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 MongoDB data directory: {data_dir}")
        return data_dir
    
    def start_mongodb(self):
        """Start MongoDB service"""
        try:
            data_dir = self.create_mongodb_data_dir()
            cmd = ["mongod", "--dbpath", str(data_dir)]
            print("🟢 Starting MongoDB...")
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='ignore'
            )
            self.processes.append(("MongoDB", process))
            
            # Wait a moment for MongoDB to start
            time.sleep(3)
            print("✅ MongoDB started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start MongoDB: {e}")
            return False
    
    def start_backend(self):
        """Start Node.js backend server"""
        try:
            backend_dir = self.project_root / "server"
            os.chdir(backend_dir)
            
            print("🟢 Starting Backend Server...")
            # Use shell=True for Windows compatibility with proper encoding
            cmd = "npm start"
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='ignore'
            )
            self.processes.append(("Backend", process))
            
            # Wait for backend to start
            time.sleep(5)
            print("✅ Backend server started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start Backend: {e}")
            return False
    
    def start_frontend(self):
        """Start React frontend"""
        try:
            frontend_dir = self.project_root / "client"
            os.chdir(frontend_dir)
            
            print("🟢 Starting Frontend...")
            # Use shell=True for Windows compatibility with proper encoding
            cmd = "npm start"
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='ignore'
            )
            self.processes.append(("Frontend", process))
            
            # Wait for frontend to start
            time.sleep(8)
            print("✅ Frontend started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start Frontend: {e}")
            return False
    
    def start_ai_service(self):
        """Start Python AI service"""
        try:
            ai_dir = self.project_root / "ai_service"
            os.chdir(ai_dir)
            
            # Check if virtual environment exists
            venv_python = ai_dir / "venv" / "Scripts" / "python.exe"
            if not venv_python.exists():
                print("⚠️  Virtual environment not found. Creating one...")
                subprocess.run(["python", "-m", "venv", "venv"], check=True)
                print("✅ Virtual environment created")
            
            print("🟢 Starting AI Service...")
            cmd = [str(venv_python), "app.py"]
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='ignore'
            )
            self.processes.append(("AI Service", process))
            
            # Wait for AI service to start
            time.sleep(3)
            print("✅ AI Service started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start AI Service: {e}")
            return False
    
    def start_all_services(self):
        """Start all services in sequence"""
        print("🚀 Starting Healthcare App Services...")
        print("=" * 50)
        # Setup for new laptops
        self.check_and_install_dependencies()
        # Start MongoDB first
        if not self.start_mongodb():
            print("❌ Failed to start MongoDB. Exiting...")
            return False
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start Backend. Exiting...")
            return False
        
        # Start AI service
        if not self.start_ai_service():
            print("⚠️  AI Service failed to start, but continuing...")
        
        # Start frontend last
        if not self.start_frontend():
            print("❌ Failed to start Frontend. Exiting...")
            return False
        
        print("=" * 50)
        print("🎉 All services started successfully!")
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:5000")
        print("🤖 AI Service: http://localhost:5001")
        print("🗄️  MongoDB: localhost:27017")
        print("\nPress Ctrl+C to stop all services")
        
        # Automatically open the frontend in the default browser
        webbrowser.open("http://localhost:3000")
        
        return True
    
    def stop_all_services(self):
        """Stop all running services"""
        print("\n🛑 Stopping all services...")
        
        for name, process in self.processes:
            try:
                print(f"🛑 Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️  Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
        
        self.processes.clear()
        print("✅ All services stopped")

def main():
    """Main function"""
    manager = ServiceManager()
    
    try:
        if manager.start_all_services():
            # Keep the script running
            while manager.running:
                time.sleep(1)
        else:
            print("❌ Failed to start services")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    finally:
        manager.stop_all_services()

if __name__ == "__main__":
    main() 