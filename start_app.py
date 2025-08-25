#!/usr/bin/env python3
"""
Healthcare Assistant App - Service Manager
Starts all services (Frontend, Backend, AI Service) with proper error handling and monitoring.
"""

import subprocess
import sys
import os
import time
import signal
import platform
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

class HealthcareServiceManager:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.processes = []
        self.is_windows = platform.system() == "Windows"
        
    def check_prerequisites(self):
        """Check if all required tools are installed"""
        logging.info("🔍 Checking prerequisites...")
        
        # Check Python
        try:
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
                logging.error("❌ Python 3.7+ is required")
                return False
            logging.info(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        except Exception as e:
            logging.error(f"❌ Python check failed: {e}")
            return False
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                logging.info(f"✅ Node.js {result.stdout.strip()}")
            else:
                logging.error("❌ Node.js is not installed")
                return False
        except FileNotFoundError:
            logging.error("❌ Node.js is not installed")
            return False
        
        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                logging.info(f"✅ npm {result.stdout.strip()}")
            else:
                logging.error("❌ npm is not installed")
                return False
        except FileNotFoundError:
            logging.error("❌ npm is not installed")
            return False
        
        return True
    
    def install_dependencies(self):
        """Install dependencies for all services"""
        logging.info("📦 Installing dependencies...")
        
        # Install Node.js dependencies for server
        try:
            server_dir = self.project_root / "server"
            logging.info("Installing server dependencies...")
            subprocess.run(['npm', 'install'], cwd=server_dir, shell=True, check=True)
            logging.info("✅ Server dependencies installed")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to install server dependencies: {e}")
            return False
        
        # Install Node.js dependencies for client
        try:
            client_dir = self.project_root / "client"
            logging.info("Installing client dependencies...")
            subprocess.run(['npm', 'install'], cwd=client_dir, shell=True, check=True)
            logging.info("✅ Client dependencies installed")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to install client dependencies: {e}")
            return False
        
        # Install Python dependencies for AI service
        try:
            ai_dir = self.project_root / "ai_service"
            logging.info("Installing AI service dependencies...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                         cwd=ai_dir, shell=True, check=True)
            logging.info("✅ AI service dependencies installed")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to install AI service dependencies: {e}")
            return False
        
        return True
    
    def start_backend(self):
        """Start Node.js backend server"""
        try:
            backend_dir = self.project_root / "server"
            
            logging.info("🟢 Starting Backend Server...")
            cmd = ['npm', 'start']
            process = subprocess.Popen(
                cmd, 
                cwd=backend_dir,
                shell=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(("Backend", process))
            
            # Wait for backend to start
            time.sleep(5)
            logging.info("✅ Backend server started successfully")
            return True
        except Exception as e:
            logging.error(f"❌ Failed to start Backend: {e}")
            return False
    
    def start_frontend(self):
        """Start React frontend"""
        try:
            frontend_dir = self.project_root / "client"
            
            logging.info("🟢 Starting Frontend...")
            cmd = ['npm', 'start']
            process = subprocess.Popen(
                cmd, 
                cwd=frontend_dir,
                shell=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(("Frontend", process))
            
            # Wait for frontend to start
            time.sleep(8)
            logging.info("✅ Frontend started successfully")
            return True
        except Exception as e:
            logging.error(f"❌ Failed to start Frontend: {e}")
            return False
    
    def start_ai_service(self):
        """Start Python AI service"""
        try:
            ai_dir = self.project_root / "ai_service"
            if not ai_dir.exists():
                logging.warning("⚠️  AI service directory not found, skipping...")
                return True
            
            logging.info("🟢 Starting AI Service...")
            # Use the new_backend.py instead of app.py
            cmd = [sys.executable, "new_backend.py"]
            process = subprocess.Popen(
                cmd, 
                cwd=ai_dir,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(("AI Service", process))
            
            # Wait for AI service to start
            time.sleep(3)
            logging.info("✅ AI Service started successfully")
            return True
        except Exception as e:
            logging.error(f"❌ Failed to start AI Service: {e}")
            return False
    
    def stop_all_services(self):
        """Stop all running services"""
        logging.info("\n🛑 Stopping all services...")
        for name, process in self.processes:
            try:
                if process.poll() is None:
                    logging.info(f"Stopping {name}...")
                    process.terminate()
                    process.wait(timeout=5)
                    logging.info(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                logging.warning(f"⚠️  Force killing {name}...")
                process.kill()
            except Exception as e:
                logging.error(f"❌ Error stopping {name}: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals"""
        logging.info("\n\n🛑 Received interrupt signal. Shutting down...")
        self.stop_all_services()
        sys.exit(0)
    
    def start_all_services(self):
        """Start all services in the correct order"""
        logging.info("🚀 Healthcare Assistant App - Starting Services")
        logging.info("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        if not self.is_windows:
            signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check prerequisites
        if not self.check_prerequisites():
            logging.error("❌ Prerequisites check failed. Please install missing dependencies.")
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            logging.error("❌ Dependency installation failed.")
            return False
        
        # Start services
        logging.info("\n🚀 Starting services...")
        
        # Start backend first
        if not self.start_backend():
            return False
        
        # Start AI service
        if not self.start_ai_service():
            logging.warning("⚠️  AI service failed to start, but continuing...")
        
        # Start frontend last
        if not self.start_frontend():
            return False
        
        logging.info("\n" + "=" * 50)
        logging.info("🎉 All services started successfully!")
        logging.info("\n📍 Access Points:")
        logging.info("   • Frontend:  http://localhost:3000")
        logging.info("   • Backend:   http://localhost:5000")
        logging.info("   • AI Service: http://localhost:5000")
        logging.info("\n💡 Press Ctrl+C to stop all services")
        logging.info("=" * 50)
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)
        
        return True

def main():
    """Main entry point"""
    manager = HealthcareServiceManager()
    success = manager.start_all_services()
    
    if not success:
        logging.error("❌ Failed to start services")
        sys.exit(1)

if __name__ == "__main__":
    main()
