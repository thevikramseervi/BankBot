"""
Perfect Database Models for BankBot
All relationships and constraints defined
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """User model with all necessary fields and relationships"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_username', 'username'),
        Index('idx_user_active', 'is_active'),
    )

class Account(Base):
    """Account model for user banking accounts"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_number = Column(String(50), unique=True, index=True, nullable=False)
    account_type = Column(String(50), nullable=False)  # checking, savings, investment
    balance = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_account_user_id', 'user_id'),
        Index('idx_account_number', 'account_number'),
        Index('idx_account_type', 'account_type'),
    )

class Transaction(Base):
    """Transaction model for banking transactions"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # credit, debit
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    account = relationship("Account", back_populates="transactions")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_transaction_account_id', 'account_id'),
        Index('idx_transaction_type', 'transaction_type'),
        Index('idx_transaction_category', 'category'),
        Index('idx_transaction_timestamp', 'timestamp'),
        Index('idx_transaction_amount', 'amount'),
    )

class ChatMessage(Base):
    """Chat message model for AI chatbot interactions"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    intent = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_chat_user_id', 'user_id'),
        Index('idx_chat_intent', 'intent'),
        Index('idx_chat_timestamp', 'timestamp'),
    )