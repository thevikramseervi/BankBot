from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from banking.models import Account, Transaction, UserProfile
from decimal import Decimal
import uuid

class Command(BaseCommand):
    help = 'Populate initial banking data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample banking data...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@bankbot.com',
                password='admin123'
            )
            self.stdout.write(f'Created superuser: {admin_user.username}')
        
        # Create sample user
        if not User.objects.filter(username='john_doe').exists():
            user = User.objects.create_user(
                username='john_doe',
                email='john@example.com',
                password='password123',
                first_name='John',
                last_name='Doe'
            )
            
            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': '+1-555-0123',
                    'address': '123 Main St, Anytown, USA',
                    'is_verified': True
                }
            )
            
            # Create checking account
            checking_account = Account.objects.create(
                user=user,
                account_number='1234-5678-9012-3456',
                account_type='checking',
                balance=Decimal('5000.00'),
                is_active=True
            )
            
            # Create savings account
            savings_account = Account.objects.create(
                user=user,
                account_number='9876-5432-1098-7654',
                account_type='savings',
                balance=Decimal('15000.00'),
                is_active=True
            )
            
            # Create sample transactions
            transactions_data = [
                {
                    'account': checking_account,
                    'transaction_type': 'deposit',
                    'amount': Decimal('5000.00'),
                    'description': 'Initial deposit',
                    'balance_after': Decimal('5000.00')
                },
                {
                    'account': checking_account,
                    'transaction_type': 'withdrawal',
                    'amount': Decimal('-150.00'),
                    'description': 'ATM withdrawal',
                    'balance_after': Decimal('4850.00')
                },
                {
                    'account': checking_account,
                    'transaction_type': 'payment',
                    'amount': Decimal('-75.50'),
                    'description': 'Online purchase',
                    'balance_after': Decimal('4774.50')
                },
                {
                    'account': savings_account,
                    'transaction_type': 'deposit',
                    'description': 'Initial deposit',
                    'amount': Decimal('15000.00'),
                    'balance_after': Decimal('15000.00')
                }
            ]
            
            for trans_data in transactions_data:
                Transaction.objects.create(
                    **trans_data,
                    reference_number=str(uuid.uuid4())
                )
            
            self.stdout.write(f'Created user: {user.username} with accounts and transactions')
        
        # Create another sample user
        if not User.objects.filter(username='jane_smith').exists():
            user = User.objects.create_user(
                username='jane_smith',
                email='jane@example.com',
                password='password123',
                first_name='Jane',
                last_name='Smith'
            )
            
            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': '+1-555-0456',
                    'address': '456 Oak Ave, Somewhere, USA',
                    'is_verified': True
                }
            )
            
            # Create checking account
            checking_account = Account.objects.create(
                user=user,
                account_number='1111-2222-3333-4444',
                account_type='checking',
                balance=Decimal('2500.00'),
                is_active=True
            )
            
            # Create sample transactions
            transactions_data = [
                {
                    'account': checking_account,
                    'transaction_type': 'deposit',
                    'amount': Decimal('2500.00'),
                    'description': 'Initial deposit',
                    'balance_after': Decimal('2500.00')
                },
                {
                    'account': checking_account,
                    'transaction_type': 'payment',
                    'amount': Decimal('-45.00'),
                    'description': 'Grocery store',
                    'balance_after': Decimal('2455.00')
                }
            ]
            
            for trans_data in transactions_data:
                Transaction.objects.create(
                    **trans_data,
                    reference_number=str(uuid.uuid4())
                )
            
            self.stdout.write(f'Created user: {user.username} with accounts and transactions')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated banking data'))