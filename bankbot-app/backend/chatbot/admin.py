from django.contrib import admin
from .models import BankingFAQ, Conversation, Message, Intent, Entity

@admin.register(BankingFAQ)
class BankingFAQAdmin(admin.ModelAdmin):
    list_display = ['intent', 'category', 'confidence_score', 'created_at']
    list_filter = ['intent', 'category', 'confidence_score', 'created_at']
    search_fields = ['question', 'answer', 'intent']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ['name', 'action', 'requires_auth', 'created_at']
    list_filter = ['requires_auth', 'created_at']
    search_fields = ['name', 'description', 'action']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_type', 'created_at']
    list_filter = ['entity_type', 'created_at']
    search_fields = ['name', 'entity_type']
    readonly_fields = ['id', 'created_at']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'message_type', 'intent_detected', 'confidence_score', 'timestamp']
    list_filter = ['message_type', 'intent_detected', 'timestamp']
    search_fields = ['content', 'conversation__session_id']
    readonly_fields = ['id', 'timestamp']
