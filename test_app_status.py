#!/usr/bin/env python3
import requests
import time

def test_app():
    print("🔍 Testing Application Status...")
    
    # Wait for React to start
    time.sleep(5)
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running successfully")
            print("🌐 Application accessible at: http://localhost:3000")
        else:
            print(f"⚠️  Frontend responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        print("⏳ Frontend may still be starting up...")

if __name__ == "__main__":
    test_app()
