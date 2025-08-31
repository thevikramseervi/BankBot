from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BankingFAQ, Conversation, Message, Intent, Entity

class BankingFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankingFAQ
        fields = ['id', 'question', 'answer', 'intent', 'category', 'confidence_score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'confidence_score', 'created_at', 'updated_at']

class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent
        fields = ['id', 'name', 'description', 'patterns', 'responses', 'action', 'requires_auth', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'name', 'entity_type', 'patterns', 'validation_rules', 'created_at']
        read_only_fields = ['id', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'session_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.StringRelatedField()
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'message_type', 'content', 'intent_detected', 'confidence_score', 'entities_extracted', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    session_id = serializers.CharField(max_length=100, required=False)
    user_id = serializers.IntegerField(required=False)

class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    intent_detected = serializers.CharField(allow_blank=True)
    confidence_score = serializers.FloatField(allow_null=True)
    entities = serializers.DictField(allow_empty=True)
    suggested_actions = serializers.ListField(child=serializers.CharField(), allow_empty=True)

class TrainingDataSerializer(serializers.Serializer):
    questions = serializers.ListField(child=serializers.CharField())
    answers = serializers.ListField(child=serializers.CharField())
    intent = serializers.CharField()
    category = serializers.CharField()