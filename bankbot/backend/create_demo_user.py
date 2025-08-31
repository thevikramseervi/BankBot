"""
Script to create a demo user for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, Base, engine
from models import User, Account
from auth import hash_password

def create_demo_user():
    """Create a demo user with accounts"""
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.email == "demo@bankbot.com").first()
        if existing_user:
            print("✅ Demo user already exists!")
            return
        
        # Create demo user
        demo_user = User(
            email="demo@bankbot.com",
            username="demo_user",
            full_name="Demo User",
            hashed_password=hash_password("demo123"),
            is_active=True
        )
        
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        
        # Create demo accounts
        checking_account = Account(
            user_id=demo_user.id,
            account_number="DEMO001",
            account_type="checking",
            balance=1234.56
        )
        
        savings_account = Account(
            user_id=demo_user.id,
            account_number="DEMO002",
            account_type="savings",
            balance=5678.90
        )
        
        db.add(checking_account)
        db.add(savings_account)
        db.commit()
        
        print("✅ Demo user created successfully!")
        print(f"   Email: demo@bankbot.com")
        print(f"   Password: demo123")
        print(f"   User ID: {demo_user.id}")
        print(f"   Accounts: {checking_account.account_number}, {savings_account.account_number}")
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()