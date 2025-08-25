#!/usr/bin/env python3
"""
Healthcare Assistant App - Service Stopper
Stops all running services gracefully.
"""

import subprocess
import sys
import platform
import psutil
import time

def find_and_kill_processes():
    """Find and kill all healthcare app related processes"""
    print("🔍 Finding healthcare app processes...")
    
    killed_processes = []
    
    # Process patterns to look for
    patterns = [
        'npm start',  # Frontend and backend
        'node index.js',  # Backend server
        'python app.py',  # AI service
        'react-scripts start',  # Frontend
        'Healthcare',  # Any process with Healthcare in name
    ]
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            
            # Check if this process matches our patterns
            for pattern in patterns:
                if pattern.lower() in cmdline.lower():
                    print(f"🎯 Found process: {proc.info['name']} (PID: {proc.info['pid']})")
                    print(f"   Command: {cmdline}")
                    
                    try:
                        proc.terminate()
                        proc.wait(timeout=5)
                        killed_processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
                        print(f"✅ Terminated {proc.info['name']}")
                    except psutil.TimeoutExpired:
                        print(f"⚠️  Force killing {proc.info['name']}...")
                        proc.kill()
                        killed_processes.append(f"{proc.info['name']} (PID: {proc.info['pid']}) - Force killed")
                    except psutil.NoSuchProcess:
                        print(f"⚠️  Process {proc.info['name']} already terminated")
                    except Exception as e:
                        print(f"❌ Error terminating {proc.info['name']}: {e}")
                    
                    break  # Don't check other patterns for this process
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process might have disappeared or we don't have access
            continue
    
    return killed_processes

def kill_processes_by_port():
    """Kill processes running on our specific ports"""
    print("\n🔍 Checking for processes on healthcare app ports...")
    
    ports = [3000, 5000, 5001]  # Frontend, Backend, AI Service
    killed_processes = []
    
    for port in ports:
        try:
            # Find processes using the port
            connections = psutil.net_connections()
            for conn in connections:
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    try:
                        proc = psutil.Process(conn.pid)
                        print(f"🎯 Found process on port {port}: {proc.name()} (PID: {conn.pid})")
                        
                        proc.terminate()
                        proc.wait(timeout=5)
                        killed_processes.append(f"{proc.name()} on port {port} (PID: {conn.pid})")
                        print(f"✅ Terminated process on port {port}")
                        
                    except psutil.TimeoutExpired:
                        print(f"⚠️  Force killing process on port {port}...")
                        proc.kill()
                        killed_processes.append(f"Process on port {port} (PID: {conn.pid}) - Force killed")
                    except psutil.NoSuchProcess:
                        print(f"⚠️  Process on port {port} already terminated")
                    except Exception as e:
                        print(f"❌ Error terminating process on port {port}: {e}")
                        
        except Exception as e:
            print(f"❌ Error checking port {port}: {e}")
    
    return killed_processes

def main():
    """Main entry point"""
    print("🛑 Healthcare Assistant App - Service Stopper")
    print("=" * 50)
    
    # Check if psutil is available
    try:
        import psutil
    except ImportError:
        print("❌ psutil is not installed. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], check=True)
            import psutil
            print("✅ psutil installed successfully")
        except Exception as e:
            print(f"❌ Failed to install psutil: {e}")
            print("Please install psutil manually: pip install psutil")
            return False
    
    # Kill processes by pattern
    killed_by_pattern = find_and_kill_processes()
    
    # Kill processes by port
    killed_by_port = kill_processes_by_port()
    
    # Summary
    all_killed = killed_by_pattern + killed_by_port
    
    print("\n" + "=" * 50)
    if all_killed:
        print("🎉 Successfully stopped the following processes:")
        for process in all_killed:
            print(f"   • {process}")
    else:
        print("ℹ️  No healthcare app processes were found running")
    
    print("\n✅ Service stopping completed!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
