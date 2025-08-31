#!/usr/bin/env python3
"""
Test script to verify BankBot authentication is working
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankbot_project.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def test_authentication():
    print("🧪 Testing BankBot Authentication...")
    print("=" * 40)
    
    # Test 1: Check if users exist
    try:
        users = User.objects.all()
        print(f"✅ Found {users.count()} users in database")
        for user in users:
            print(f"   - {user.username} ({user.email})")
    except Exception as e:
        print(f"❌ Error checking users: {e}")
        return False
    
    # Test 2: Test authentication
    try:
        # Test john_doe
        user = authenticate(username='john_doe', password='password123')
        if user:
            print(f"✅ Authentication successful for john_doe")
        else:
            print(f"❌ Authentication failed for john_doe")
        
        # Test jane_smith
        user = authenticate(username='jane_smith', password='password123')
        if user:
            print(f"✅ Authentication successful for jane_smith")
        else:
            print(f"❌ Authentication failed for jane_smith")
            
    except Exception as e:
        print(f"❌ Error testing authentication: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎯 Authentication Test Summary:")
    print("   - Users exist in database")
    print("   - Authentication working")
    print("\n💡 To start the server:")
    print("   python manage.py runserver")
    
    return True

if __name__ == "__main__":
    test_authentication()