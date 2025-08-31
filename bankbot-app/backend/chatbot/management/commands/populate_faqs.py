from django.core.management.base import BaseCommand
from chatbot.models import BankingFAQ, Intent, Entity

class Command(BaseCommand):
    help = 'Populate initial FAQ training data for the chatbot'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample FAQ training data...')
        
        # Create intents
        intents_data = [
            {
                'name': 'check_balance',
                'description': 'User wants to check their account balance',
                'patterns': [
                    'What is my balance?',
                    'How much money do I have?',
                    'Check my balance',
                    'Show me my balance',
                    'What\'s in my account?'
                ],
                'responses': [
                    'Your current balance is available in your banking portal.',
                    'I can help you check your balance. Please log in to view your accounts.'
                ],
                'action': 'check_balance',
                'requires_auth': True
            },
            {
                'name': 'transfer_money',
                'description': 'User wants to transfer money between accounts',
                'patterns': [
                    'I want to transfer money',
                    'Transfer funds',
                    'Send money to another account',
                    'Move money between accounts',
                    'How do I transfer money?'
                ],
                'responses': [
                    'I can help you with transfers. Please use the transfer form in your banking portal.',
                    'To transfer money, you\'ll need the destination account number and amount.'
                ],
                'action': 'transfer_money',
                'requires_auth': True
            },
            {
                'name': 'transaction_history',
                'description': 'User wants to view transaction history',
                'patterns': [
                    'Show me my transactions',
                    'Transaction history',
                    'Recent transactions',
                    'Where can I see my transactions?',
                    'Account statement'
                ],
                'responses': [
                    'Your transaction history is available in the transactions tab of your banking portal.',
                    'I can show you recent transactions. Check the transactions section for details.'
                ],
                'action': 'transaction_history',
                'requires_auth': True
            },
            {
                'name': 'account_info',
                'description': 'User wants information about their accounts',
                'patterns': [
                    'Tell me about my accounts',
                    'Account information',
                    'What accounts do I have?',
                    'Account details',
                    'My banking accounts'
                ],
                'responses': [
                    'I can show you your account information. Please log in to view details.',
                    'Your account details are available in the accounts section of your portal.'
                ],
                'action': 'account_info',
                'requires_auth': True
            },
            {
                'name': 'general_help',
                'description': 'User needs general banking help',
                'patterns': [
                    'Help',
                    'I need help',
                    'What can you do?',
                    'How can you help me?',
                    'Banking assistance'
                ],
                'responses': [
                    'I\'m here to help with your banking needs! I can help you check balances, view transactions, transfer money, and answer questions about your accounts.',
                    'I\'m your banking assistant. I can help with account information, transfers, and general banking questions.'
                ],
                'action': 'general_help',
                'requires_auth': False
            }
        ]
        
        for intent_data in intents_data:
            intent, created = Intent.objects.get_or_create(
                name=intent_data['name'],
                defaults=intent_data
            )
            if created:
                self.stdout.write(f'Created intent: {intent.name}')
        
        # Create FAQ entries
        faqs_data = [
            {
                'question': 'What is my current balance?',
                'answer': 'You can check your current balance by logging into your banking portal and viewing the accounts section. I can also provide a quick balance overview if you\'re logged in.',
                'intent': 'check_balance',
                'category': 'account_inquiry',
                'confidence_score': 0.9
            },
            {
                'question': 'How do I transfer money to another account?',
                'answer': 'To transfer money, you\'ll need the destination account number and the amount you want to transfer. You can complete transfers through the transfer form in your banking portal.',
                'intent': 'transfer_money',
                'category': 'transfers',
                'confidence_score': 0.9
            },
            {
                'question': 'Where can I see my transaction history?',
                'answer': 'Your transaction history is available in the transactions tab of your banking portal. You can view recent transactions, download statements, and filter by date or transaction type.',
                'intent': 'transaction_history',
                'category': 'transactions',
                'confidence_score': 0.9
            },
            {
                'question': 'What types of accounts do you offer?',
                'answer': 'We offer several types of accounts including checking accounts for daily transactions, savings accounts for earning interest, and credit accounts. Each has different features and benefits.',
                'intent': 'account_info',
                'category': 'accounts',
                'confidence_score': 0.8
            },
            {
                'question': 'How do I reset my password?',
                'answer': 'To reset your password, go to the login page and click on "Forgot Password". You\'ll receive a reset link via email or can answer security questions to verify your identity.',
                'intent': 'general_help',
                'category': 'security',
                'confidence_score': 0.8
            },
            {
                'question': 'What are your banking hours?',
                'answer': 'Our online banking portal is available 24/7. Branch locations typically operate Monday through Friday from 9 AM to 5 PM, with some locations offering extended hours.',
                'intent': 'general_help',
                'category': 'hours',
                'confidence_score': 0.8
            },
            {
                'question': 'How do I report a lost or stolen card?',
                'answer': 'If your card is lost or stolen, please call our 24/7 customer service line immediately. We can freeze your card and issue a replacement to prevent unauthorized transactions.',
                'intent': 'general_help',
                'category': 'security',
                'confidence_score': 0.9
            },
            {
                'question': 'What fees are associated with my account?',
                'answer': 'Account fees vary by account type and features. Common fees include monthly maintenance fees, ATM fees, and overdraft fees. You can view your specific fee schedule in your account details.',
                'intent': 'account_info',
                'category': 'fees',
                'confidence_score': 0.8
            }
        ]
        
        for faq_data in faqs_data:
            faq, created = BankingFAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.question[:50]}...')
        
        # Create entities
        entities_data = [
            {
                'name': 'amount',
                'entity_type': 'currency',
                'patterns': [r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*dollars?'],
                'validation_rules': {'min_value': 0.01, 'max_value': 999999.99}
            },
            {
                'name': 'account_number',
                'entity_type': 'identifier',
                'patterns': [r'\b(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})\b', r'\b(\d{8,16})\b'],
                'validation_rules': {'format': 'XXXX-XXXX-XXXX-XXXX', 'length': 16}
            },
            {
                'name': 'date',
                'entity_type': 'temporal',
                'patterns': [r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b', r'\b(\d{4}-\d{2}-\d{2})\b'],
                'validation_rules': {'format': 'MM/DD/YYYY'}
            }
        ]
        
        for entity_data in entities_data:
            entity, created = Entity.objects.get_or_create(
                name=entity_data['name'],
                defaults=entity_data
            )
            if created:
                self.stdout.write(f'Created entity: {entity.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated FAQ training data'))