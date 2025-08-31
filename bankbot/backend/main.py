"""
BankBot - Modern AI Banking Assistant
Built with FastAPI, SQLAlchemy, and Pydantic
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from datetime import datetime
from typing import List

from database import engine, Base
from models import User, Account, Transaction, ChatMessage
from schemas import (
    UserCreate, UserLogin, UserResponse, 
    AccountResponse, TransactionResponse,
    ChatRequest, ChatResponse, BalanceResponse
)
from auth import create_access_token, get_current_user, hash_password, verify_password
from chatbot import BankBot

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize BankBot
bankbot = BankBot()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 BankBot starting up...")
    yield
    # Shutdown
    print("🛑 BankBot shutting down...")

# Create FastAPI app
app = FastAPI(
    title="BankBot API",
    description="Modern AI-powered banking assistant API",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "BankBot API is running! 🚀",
        "version": "2.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "docs": "/docs",
            "auth": "/api/auth",
            "banking": "/api/banking",
            "chat": "/api/chat"
        }
    }

# Authentication endpoints
@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    from database import get_db
    db = next(get_db())
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create default account
    default_account = Account(
        user_id=new_user.id,
        account_number=f"ACC{new_user.id:06d}",
        account_type="checking",
        balance=1000.00  # Welcome bonus
    )
    db.add(default_account)
    db.commit()
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        full_name=new_user.full_name,
        created_at=new_user.created_at
    )

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    """Login user and return access token"""
    from database import get_db
    db = next(get_db())
    
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            created_at=user.created_at
        )
    }

# Banking endpoints
@app.get("/api/banking/accounts", response_model=List[AccountResponse])
async def get_accounts(current_user: User = Depends(get_current_user)):
    """Get user's accounts"""
    from database import get_db
    db = next(get_db())
    
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    return accounts

@app.get("/api/banking/balance", response_model=BalanceResponse)
async def get_balance(current_user: User = Depends(get_current_user)):
    """Get user's total balance across all accounts"""
    from database import get_db
    db = next(get_db())
    
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    total_balance = sum(account.balance for account in accounts)
    
    return BalanceResponse(
        total_balance=total_balance,
        accounts=[
            AccountResponse(
                id=acc.id,
                account_number=acc.account_number,
                account_type=acc.account_type,
                balance=acc.balance,
                user_id=acc.user_id,
                created_at=acc.created_at
            ) for acc in accounts
        ]
    )

@app.get("/api/banking/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """Get user's recent transactions"""
    from database import get_db
    db = next(get_db())
    
    # Get transactions from user's accounts
    user_accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    account_ids = [acc.id for acc in user_accounts]
    
    transactions = db.query(Transaction).filter(
        Transaction.account_id.in_(account_ids)
    ).order_by(Transaction.timestamp.desc()).limit(limit).all()
    
    return transactions

# Chatbot endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_bot(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Chat with BankBot AI assistant"""
    try:
        # Get user context for personalized responses
        from database import get_db
        db = next(get_db())
        
        user_accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
        user_balance = sum(acc.balance for acc in user_accounts)
        
        # Get response from BankBot
        response = bankbot.get_response(
            message=chat_request.message,
            user_context={
                "user_id": current_user.id,
                "username": current_user.username,
                "balance": user_balance,
                "accounts": len(user_accounts)
            }
        )
        
        return ChatResponse(
            response=response["message"],
            intent=response["intent"],
            confidence=response["confidence"],
            suggested_actions=response["suggested_actions"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )