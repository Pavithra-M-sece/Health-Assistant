#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""

import requests
import json

def test_auth_endpoints():
    """Test the authentication endpoints"""
    base_url = "http://localhost:5000/api/auth"
    
    print("🔐 Testing Authentication Endpoints")
    print("=" * 50)
    
    # Test 1: Register endpoint
    print("\n1️⃣ Testing Registration")
    register_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/register",
            json=register_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
        elif response.status_code == 400:
            data = response.json()
            if "already exists" in data.get('message', ''):
                print("ℹ️ User already exists (expected)")
            else:
                print(f"❌ Registration failed: {data.get('message')}")
        else:
            print(f"❌ Registration failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test 2: Login endpoint
    print("\n2️⃣ Testing Login")
    login_data = {
        "username": "testuser123",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/login",
            json=login_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print("✅ Login successful!")
                print(f"Token received: {data['token'][:20]}...")
            else:
                print("❌ Login response missing token")
        else:
            print(f"❌ Login failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Test 3: Health check
    print("\n3️⃣ Testing Health Check")
    try:
        response = requests.get(
            "http://localhost:5000/api/health",
            timeout=5
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Health check successful!")
        else:
            print(f"❌ Health check failed")
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Authentication test completed!")

if __name__ == "__main__":
    test_auth_endpoints()
