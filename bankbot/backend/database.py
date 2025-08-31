"""
Perfect Database Configuration for BankBot
Automatically handles all database operations
"""

import os
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file path - will be created automatically
DATABASE_PATH = os.path.join(BASE_DIR, "bankbot.db")

# SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine with optimized settings
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    },
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=False  # Set to True for debugging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database dependency
def get_db():
    """Get database session with automatic cleanup"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database with sample data"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Check if we need to add sample data
        db = next(get_db())
        
        # Import models here to avoid circular imports
        from models import User, Account, Transaction
        from auth import hash_password
        
        # Check if demo user exists
        existing_user = db.query(User).filter(User.email == "demo@bankbot.com").first()
        
        if not existing_user:
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
            
            # Create sample transactions
            sample_transactions = [
                Transaction(
                    account_id=checking_account.id,
                    transaction_type="credit",
                    amount=500.00,
                    description="Salary Deposit",
                    category="income"
                ),
                Transaction(
                    account_id=checking_account.id,
                    transaction_type="debit",
                    amount=45.67,
                    description="Grocery Store",
                    category="food"
                ),
                Transaction(
                    account_id=checking_account.id,
                    transaction_type="debit",
                    amount=89.99,
                    description="Online Shopping",
                    category="shopping"
                ),
                Transaction(
                    account_id=savings_account.id,
                    transaction_type="credit",
                    amount=1000.00,
                    description="Transfer from Checking",
                    category="transfer"
                )
            ]
            
            for transaction in sample_transactions:
                db.add(transaction)
            
            db.commit()
            print("✅ Database initialized with demo data")
        else:
            print("✅ Database already contains demo data")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

def get_database_info():
    """Get database information"""
    try:
        # Check if database file exists
        if os.path.exists(DATABASE_PATH):
            file_size = os.path.getsize(DATABASE_PATH)
            return {
                "exists": True,
                "path": DATABASE_PATH,
                "size_bytes": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2)
            }
        else:
            return {
                "exists": False,
                "path": DATABASE_PATH,
                "size_bytes": 0,
                "size_mb": 0
            }
    except Exception as e:
        return {
            "error": str(e),
            "path": DATABASE_PATH
        }