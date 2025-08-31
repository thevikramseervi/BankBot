from django.contrib import admin
from .models import Account, Transaction, Transfer, UserProfile

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'account_type', 'balance', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['account_number', 'user__username', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'account', 'transaction_type', 'amount', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['reference_number', 'account__account_number', 'description']
    readonly_fields = ['id', 'reference_number', 'created_at']

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_account', 'to_account', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['from_account__account_number', 'to_account__account_number']
    readonly_fields = ['id', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
