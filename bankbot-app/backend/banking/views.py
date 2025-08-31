from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
import uuid
from .models import Account, Transaction, Transfer, UserProfile
from .serializers import (
    AccountSerializer, TransactionSerializer, TransferSerializer,
    CreateTransferSerializer, AccountBalanceSerializer, TransactionHistorySerializer,
    UserProfileSerializer
)

class AccountViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer
    
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def balance(self, request):
        """Get account balances for the authenticated user"""
        accounts = self.get_queryset()
        serializer = AccountBalanceSerializer(accounts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """Get transaction history for a specific account"""
        try:
            account = self.get_queryset().get(pk=pk)
            transactions = Transaction.objects.filter(account=account)
            serializer = TransactionHistorySerializer(transactions, many=True)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response(
                {'error': 'Account not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)

class TransferViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransferSerializer
    
    def get_queryset(self):
        return Transfer.objects.filter(from_account__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create a new transfer"""
        serializer = CreateTransferSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Get the user's account (assuming they have one checking account)
                    from_account = Account.objects.filter(
                        user=request.user, 
                        account_type='checking',
                        is_active=True
                    ).first()
                    
                    if not from_account:
                        return Response(
                            {'error': 'No active checking account found'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Get the destination account
                    to_account = Account.objects.filter(
                        account_number=serializer.validated_data['to_account_number'],
                        is_active=True
                    ).first()
                    
                    if not to_account:
                        return Response(
                            {'error': 'Destination account not found'}, 
                            status=status.HTTP_404_NOT_FOUND
                        )
                    
                    if from_account == to_account:
                        return Response(
                            {'error': 'Cannot transfer to the same account'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    amount = serializer.validated_data['amount']
                    if from_account.balance < amount:
                        return Response(
                            {'error': 'Insufficient funds'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Create transfer
                    transfer = Transfer.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        amount=amount,
                        description=serializer.validated_data.get('description', '')
                    )
                    
                    # Update account balances
                    from_account.balance -= amount
                    from_account.save()
                    
                    to_account.balance += amount
                    to_account.save()
                    
                    # Create transactions
                    Transaction.objects.create(
                        account=from_account,
                        transaction_type='transfer',
                        amount=-amount,
                        description=f"Transfer to {to_account.account_number}",
                        balance_after=from_account.balance,
                        reference_number=str(uuid.uuid4())
                    )
                    
                    Transaction.objects.create(
                        account=to_account,
                        transaction_type='transfer',
                        amount=amount,
                        description=f"Transfer from {from_account.account_number}",
                        balance_after=to_account.balance,
                        reference_number=str(uuid.uuid4())
                    )
                    
                    # Mark transfer as completed
                    transfer.status = 'completed'
                    transfer.completed_at = timezone.now()
                    transfer.save()
                    
                    return Response(
                        TransferSerializer(transfer).data, 
                        status=status.HTTP_201_CREATED
                    )
                    
            except Exception as e:
                return Response(
                    {'error': f'Transfer failed: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class BankingStatsViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get banking summary for the authenticated user"""
        accounts = Account.objects.filter(user=request.user, is_active=True)
        total_balance = sum(account.balance for account in accounts)
        
        recent_transactions = Transaction.objects.filter(
            account__user=request.user
        ).order_by('-created_at')[:5]
        
        pending_transfers = Transfer.objects.filter(
            from_account__user=request.user,
            status='pending'
        ).count()
        
        return Response({
            'total_balance': total_balance,
            'account_count': accounts.count(),
            'recent_transactions': TransactionHistorySerializer(recent_transactions, many=True).data,
            'pending_transfers': pending_transfers
        })
