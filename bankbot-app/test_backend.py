#!/usr/bin/env python3
"""
Test script to verify BankBot backend is working correctly
"""

import requests
import time
import sys

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing BankBot Backend...")
    print("=" * 40)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running")
        else:
            print(f"⚠️  Django server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Django server is not running. Please start it first.")
        print("   Run: cd backend && python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error testing Django server: {e}")
        return False
    
    # Test 2: Check banking API
    try:
        response = requests.get(f"{base_url}/api/banking/accounts/", timeout=5)
        if response.status_code == 401:  # Unauthorized - expected for unauthenticated requests
            print("✅ Banking API is accessible (authentication required)")
        else:
            print(f"⚠️  Banking API responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing Banking API: {e}")
    
    # Test 3: Check chatbot API
    try:
        response = requests.get(f"{base_url}/api/chatbot/faqs/", timeout=5)
        if response.status_code == 200:
            print("✅ Chatbot API is accessible")
        else:
            print(f"⚠️  Chatbot API responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing Chatbot API: {e}")
    
    # Test 4: Check admin interface
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        if response.status_code == 200:
            print("✅ Admin interface is accessible")
        else:
            print(f"⚠️  Admin interface responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing Admin interface: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Backend Test Summary:")
    print("   - Django server should be running on http://localhost:8000")
    print("   - Admin interface: http://localhost:8000/admin")
    print("   - API endpoints: http://localhost:8000/api/")
    print("\n💡 To start the backend:")
    print("   cd backend")
    print("   source venv/bin/activate")
    print("   python manage.py runserver")
    
    return True

if __name__ == "__main__":
    test_backend()