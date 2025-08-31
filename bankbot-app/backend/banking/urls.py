from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'transfers', views.TransferViewSet, basename='transfer')
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'stats', views.BankingStatsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
]