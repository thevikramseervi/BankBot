"""
Perfect Pydantic Schemas for BankBot
Comprehensive validation and examples included
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime
import re

# User schemas
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    full_name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

class UserResponse(UserBase):
    id: int = Field(..., description="User's unique ID")
    created_at: datetime = Field(..., description="Account creation timestamp")
    is_active: bool = Field(..., description="Whether the account is active")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "email": "demo@bankbot.com",
                "username": "demo_user",
                "full_name": "Demo User",
                "created_at": "2024-01-01T00:00:00Z",
                "is_active": True
            }
        }

# Account schemas
class AccountBase(BaseModel):
    account_number: str = Field(..., description="Account number")
    account_type: str = Field(..., description="Type of account (checking, savings, investment)")
    balance: float = Field(..., ge=0, description="Current account balance")
    
    @validator('account_type')
    def validate_account_type(cls, v):
        allowed_types = ['checking', 'savings', 'investment']
        if v.lower() not in allowed_types:
            raise ValueError(f'Account type must be one of: {", ".join(allowed_types)}')
        return v.lower()

class AccountResponse(AccountBase):
    id: int = Field(..., description="Account's unique ID")
    user_id: int = Field(..., description="Owner's user ID")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "account_number": "DEMO001",
                "account_type": "checking",
                "balance": 1234.56,
                "user_id": 1,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }

# Transaction schemas
class TransactionBase(BaseModel):
    transaction_type: str = Field(..., description="Type of transaction (credit, debit)")
    amount: float = Field(..., gt=0, description="Transaction amount")
    description: str = Field(..., min_length=1, max_length=255, description="Transaction description")
    category: str = Field(..., min_length=1, max_length=100, description="Transaction category")
    
    @validator('transaction_type')
    def validate_transaction_type(cls, v):
        if v.lower() not in ['credit', 'debit']:
            raise ValueError('Transaction type must be either "credit" or "debit"')
        return v.lower()

class TransactionResponse(TransactionBase):
    id: int = Field(..., description="Transaction's unique ID")
    account_id: int = Field(..., description="Associated account ID")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "transaction_type": "credit",
                "amount": 500.00,
                "description": "Salary Deposit",
                "category": "income",
                "account_id": 1,
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }

# Balance schemas
class BalanceResponse(BaseModel):
    total_balance: float = Field(..., ge=0, description="Total balance across all accounts")
    accounts: List[AccountResponse] = Field(..., description="List of user accounts")
    
    class Config:
        schema_extra = {
            "example": {
                "total_balance": 6913.46,
                "accounts": [
                    {
                        "id": 1,
                        "account_number": "DEMO001",
                        "account_type": "checking",
                        "balance": 1234.56,
                        "user_id": 1,
                        "created_at": "2024-01-01T00:00:00Z"
                    },
                    {
                        "id": 2,
                        "account_number": "DEMO002",
                        "account_type": "savings",
                        "balance": 5678.90,
                        "user_id": 1,
                        "created_at": "2024-01-01T00:00:00Z"
                    }
                ]
            }
        }

# Chat schemas
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User's message to the chatbot")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What's my current balance?",
                "session_id": "session_123"
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(..., description="Chatbot's response")
    intent: str = Field(..., description="Detected intent of the user's message")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score of intent detection")
    suggested_actions: List[str] = Field(..., description="Suggested actions for the user")
    
    class Config:
        schema_extra = {
            "example": {
                "response": "Your current balance is $6,913.46. You have 2 account(s).",
                "intent": "balance",
                "confidence": 0.95,
                "suggested_actions": ["View detailed balance", "Check other accounts", "Download statement"]
            }
        }

# Token schemas
class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (usually 'bearer')")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    email: Optional[str] = Field(None, description="User's email from token")

# Health check schema
class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    database: dict = Field(..., description="Database status information")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "2.0.0",
                "database": {
                    "exists": True,
                    "size_mb": 0.12
                }
            }
        }