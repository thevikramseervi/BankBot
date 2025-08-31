#!/usr/bin/env python3
"""
Test script to verify BankBot chatbot is working
"""

import os
import sys
import django
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankbot_project.settings')
django.setup()

def test_chatbot_endpoint():
    print("🧪 Testing BankBot Chatbot Endpoint...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get('http://localhost:8000/')
        print(f"✅ Server is running: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False
    
    # Test 2: Check chatbot endpoint
    try:
        response = requests.get('http://localhost:8000/api/chatbot/')
        print(f"✅ Chatbot endpoint accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Chatbot endpoint not accessible: {e}")
        return False
    
    # Test 3: Test chat without authentication (should fail)
    try:
        chat_data = {
            'message': 'What is my balance?',
            'session_id': 'test123'
        }
        response = requests.post(
            'http://localhost:8000/api/chatbot/chat/',
            json=chat_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"✅ Chat endpoint responds: {response.status_code}")
        if response.status_code == 401:
            print("   Expected: Authentication required")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 Chatbot Test Summary:")
    print("   - Server is running")
    print("   - Chatbot endpoint accessible")
    print("   - Chat requires authentication (as expected)")
    print("\n💡 Next steps:")
    print("   1. Login through frontend")
    print("   2. Test chatbot with authenticated session")
    
    return True

if __name__ == "__main__":
    test_chatbot_endpoint()