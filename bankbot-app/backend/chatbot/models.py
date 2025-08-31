from django.db import models
from django.contrib.auth.models import User
import uuid

class BankingFAQ(models.Model):
    """Model to store banking FAQ training data"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField()
    intent = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.intent}: {self.question[:50]}..."
    
    class Meta:
        ordering = ['-confidence_score', '-created_at']

class Conversation(models.Model):
    """Model to store conversation history"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation {self.session_id} - {self.user.username}"
    
    class Meta:
        ordering = ['-updated_at']

class Message(models.Model):
    """Model to store individual messages in conversations"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    intent_detected = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    entities_extracted = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."
    
    class Meta:
        ordering = ['timestamp']

class Intent(models.Model):
    """Model to store intent patterns and responses"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    patterns = models.JSONField(default=list)  # List of training patterns
    responses = models.JSONField(default=list)  # List of possible responses
    action = models.CharField(max_length=100, blank=True)  # Action to perform
    requires_auth = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Entity(models.Model):
    """Model to store entity extraction patterns"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=50)  # e.g., 'amount', 'account_number', 'date'
    patterns = models.JSONField(default=list)  # Regex patterns for extraction
    validation_rules = models.JSONField(default=dict)  # Validation rules
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.entity_type})"
    
    class Meta:
        ordering = ['name']
