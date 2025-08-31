"""
Perfect Main FastAPI Application for BankBot
Comprehensive banking API with automatic setup
"""

import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Add backend directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_database, get_database_info
from models import User, Account, Transaction, ChatMessage
from schemas import (
    UserCreate, UserLogin, UserResponse, 
    AccountResponse, TransactionResponse,
    ChatRequest, ChatResponse, BalanceResponse,
    HealthResponse
)
from auth import (
    create_access_token, create_refresh_token, get_current_user, 
    get_current_active_user, hash_password, verify_password,
    validate_password_strength, generate_secure_password,
    login_rate_limiter
)
from chatbot import BankBot

# Global variables
VERSION = "2.0.0"
APP_NAME = "BankBot API"
APP_DESCRIPTION = "Perfect AI-powered banking assistant API with zero configuration needed"

# Initialize BankBot
bankbot = BankBot()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 BankBot starting up...")
    print("🔧 Initializing database...")
    
    try:
        # Initialize database with sample data
        init_database()
        print("✅ Database initialized successfully")
        
        # Get database info
        db_info = get_database_info()
        if db_info.get("exists"):
            print(f"📊 Database size: {db_info.get('size_mb', 0)} MB")
        else:
            print("⚠️  Database file not found")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    
    print("🤖 BankBot AI initialized")
    print("🌐 Application ready to serve requests")
    
    yield
    
    # Shutdown
    print("🛑 BankBot shutting down...")
    print("👋 Goodbye!")

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed feedback"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with application information"""
    return {
        "message": "BankBot API is running! 🚀",
        "version": VERSION,
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "auth": "/api/auth",
            "banking": "/api/banking",
            "chat": "/api/chat"
        },
        "features": [
            "AI-powered banking assistant",
            "Secure authentication",
            "Account management",
            "Transaction tracking",
            "Real-time responses"
        ]
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    db_info = get_database_info()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=VERSION,
        database=db_info
    )

# Authentication endpoints
@app.post("/api/auth/register", response_model=UserResponse, tags=["Authentication"])
async def register(user_data: UserCreate):
    """Register a new user with comprehensive validation"""
    from database import get_db
    
    # Validate password strength
    password_validation = validate_password_strength(user_data.password)
    if not password_validation["is_valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password does not meet security requirements",
                "errors": password_validation["errors"],
                "warnings": password_validation["warnings"],
                "strength_score": password_validation["strength_score"]
            }
        )
    
    db = next(get_db())
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
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
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )
    finally:
        db.close()

@app.post("/api/auth/login", tags=["Authentication"])
async def login(user_data: UserLogin, request: Request):
    """Login user with rate limiting and return access token"""
    from database import get_db
    
    # Rate limiting
    client_ip = request.client.host
    if not login_rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )
    
    db = next(get_db())
    
    try:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is deactivated"
            )
        
        # Create tokens
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 30 * 60,  # 30 minutes
            "user": UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                created_at=user.created_at
            )
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
    finally:
        db.close()

@app.post("/api/auth/refresh", tags=["Authentication"])
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    from database import get_db
    
    try:
        # Verify refresh token
        email = verify_token(refresh_token, "refresh")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new access token
        new_access_token = create_access_token(data={"sub": email})
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 30 * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

# Banking endpoints
@app.get("/api/banking/accounts", response_model=List[AccountResponse], tags=["Banking"])
async def get_accounts(current_user: User = Depends(get_current_active_user)):
    """Get user's accounts with detailed information"""
    from database import get_db
    
    db = next(get_db())
    
    try:
        accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
        return accounts
    finally:
        db.close()

@app.get("/api/banking/balance", response_model=BalanceResponse, tags=["Banking"])
async def get_balance(current_user: User = Depends(get_current_active_user)):
    """Get user's total balance across all accounts"""
    from database import get_db
    
    db = next(get_db())
    
    try:
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
    finally:
        db.close()

@app.get("/api/banking/transactions", response_model=List[TransactionResponse], tags=["Banking"])
async def get_transactions(
    limit: int = 10,
    offset: int = 0,
    account_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's transactions with filtering and pagination"""
    from database import get_db
    
    db = next(get_db())
    
    try:
        # Get user's accounts
        user_accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
        account_ids = [acc.id for acc in user_accounts]
        
        # Build query
        query = db.query(Transaction).filter(Transaction.account_id.in_(account_ids))
        
        # Apply filters
        if account_id:
            if account_id not in account_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid account ID"
                )
            query = query.filter(Transaction.account_id == account_id)
        
        if transaction_type:
            if transaction_type.lower() not in ['credit', 'debit']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid transaction type"
                )
            query = query.filter(Transaction.transaction_type == transaction_type.lower())
        
        if category:
            query = query.filter(Transaction.category.ilike(f"%{category}%"))
        
        # Apply pagination and ordering
        transactions = query.order_by(Transaction.timestamp.desc()).offset(offset).limit(limit).all()
        
        return transactions
    finally:
        db.close()

# Chatbot endpoint
@app.post("/api/chat", response_model=ChatResponse, tags=["Chatbot"])
async def chat_with_bot(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Chat with BankBot AI assistant"""
    try:
        from database import get_db
        
        db = next(get_db())
        
        try:
            # Get user context for personalized responses
            user_accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
            user_balance = sum(acc.balance for acc in user_accounts)
            
            # Get response from BankBot
            response = bankbot.get_response(
                message=chat_request.message,
                user_context={
                    "user_id": current_user.id,
                    "username": current_user.username,
                    "balance": user_balance,
                    "accounts": len(user_accounts),
                    "session_id": chat_request.session_id
                }
            )
            
            # Store chat message in database
            chat_message = ChatMessage(
                user_id=current_user.id,
                message=chat_request.message,
                response=response["message"],
                intent=response["intent"],
                confidence=response["confidence"]
            )
            db.add(chat_message)
            db.commit()
            
            return ChatResponse(
                response=response["message"],
                intent=response["intent"],
                confidence=response["confidence"],
                suggested_actions=response["suggested_actions"]
            )
            
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )

# Utility endpoints
@app.get("/api/chat/suggestions", tags=["Chatbot"])
async def get_chat_suggestions():
    """Get suggested questions for the chatbot"""
    return {
        "suggestions": bankbot.get_suggested_questions(),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/auth/password/validate", tags=["Authentication"])
async def validate_password(password: str):
    """Validate password strength"""
    return validate_password_strength(password)

@app.post("/api/auth/password/generate", tags=["Authentication"])
async def generate_password(length: int = 16):
    """Generate a secure password"""
    if length < 8 or length > 64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password length must be between 8 and 64 characters"
        )
    
    return {
        "password": generate_secure_password(length),
        "length": length,
        "timestamp": datetime.now().isoformat()
    }

# Error handling for unmatched routes
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    """Catch all unmatched routes"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Endpoint '/{full_path}' not found. Check /docs for available endpoints."
    )

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting BankBot API...")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔍 Alternative Docs: http://localhost:8000/redoc")
    print(f"💚 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )