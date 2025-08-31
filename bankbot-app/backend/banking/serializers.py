from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Transaction, Transfer, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'address', 'date_of_birth', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'user', 'account_number', 'account_type', 'balance', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'account_number', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'description', 'balance_after', 'reference_number', 'created_at']
        read_only_fields = ['id', 'account', 'balance_after', 'reference_number', 'created_at']

class TransferSerializer(serializers.ModelSerializer):
    from_account = AccountSerializer(read_only=True)
    to_account = AccountSerializer(read_only=True)
    
    class Meta:
        model = Transfer
        fields = ['id', 'from_account', 'to_account', 'amount', 'description', 'status', 'transfer_fee', 'created_at', 'completed_at']
        read_only_fields = ['id', 'from_account', 'status', 'transfer_fee', 'created_at', 'completed_at']

class CreateTransferSerializer(serializers.ModelSerializer):
    to_account_number = serializers.CharField(max_length=20)
    
    class Meta:
        model = Transfer
        fields = ['to_account_number', 'amount', 'description']
    
    def validate(self, data):
        amount = data.get('amount')
        if amount <= 0:
            raise serializers.ValidationError("Transfer amount must be greater than 0")
        return data

class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'account_type', 'balance', 'is_active']

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'balance_after', 'reference_number', 'created_at']