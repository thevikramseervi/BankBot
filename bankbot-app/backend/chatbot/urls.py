from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'faqs', views.BankingFAQViewSet, basename='faq')
router.register(r'intents', views.IntentViewSet, basename='intent')
router.register(r'entities', views.EntityViewSet, basename='entity')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'chat', views.ChatbotViewSet, basename='chatbot')

urlpatterns = [
    path('', include(router.urls)),
]