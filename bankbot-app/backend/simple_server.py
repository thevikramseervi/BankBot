#!/usr/bin/env python3
"""
Simple test server to debug Django startup issues
"""

import os
import sys
import django

def test_django_setup():
    print("🧪 Testing Django Setup...")
    print("=" * 40)
    
    try:
        # Setup Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankbot_project.settings')
        print("✅ Django settings module set")
        
        django.setup()
        print("✅ Django setup completed")
        
        # Test imports
        from django.contrib.auth.models import User
        print("✅ User model imported")
        
        from banking.models import Account
        print("✅ Banking models imported")
        
        from chatbot.models import BankingFAQ
        print("✅ Chatbot models imported")
        
        # Test database connection
        user_count = User.objects.count()
        print(f"✅ Database connection working: {user_count} users found")
        
        faq_count = BankingFAQ.objects.count()
        print(f"✅ FAQ data available: {faq_count} FAQs found")
        
        print("\n🎯 Django Setup Test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Django Setup Test: FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_django_setup()