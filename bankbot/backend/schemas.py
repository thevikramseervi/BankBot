"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Account schemas
class AccountBase(BaseModel):
    account_number: str
    account_type: str
    balance: float

class AccountResponse(AccountBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Transaction schemas
class TransactionBase(BaseModel):
    transaction_type: str
    amount: float
    description: str
    category: str

class TransactionResponse(TransactionBase):
    id: int
    account_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Balance schemas
class BalanceResponse(BaseModel):
    total_balance: float
    accounts: List[AccountResponse]

# Chat schemas
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    suggested_actions: List[str]

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None