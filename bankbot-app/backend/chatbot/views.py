from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pandas as pd
from .models import BankingFAQ, Conversation, Message, Intent, Entity
from .serializers import (
    BankingFAQSerializer, IntentSerializer, EntitySerializer,
    ConversationSerializer, MessageSerializer, ChatMessageSerializer,
    ChatResponseSerializer, TrainingDataSerializer
)

class BankingFAQViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = BankingFAQ.objects.all()
    serializer_class = BankingFAQSerializer

class IntentViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Intent.objects.all()
    serializer_class = IntentSerializer

class EntityViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

class ConversationViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(conversation__user=self.request.user)

class ChatbotViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vectorizer = None
        self.classifier = None
        self._load_nlu_model()
    
    def _load_nlu_model(self):
        """Load and train the NLU model"""
        try:
            # Get training data from database
            faqs = BankingFAQ.objects.all()
            if faqs.exists():
                # Prepare training data
                questions = [faq.question for faq in faqs]
                intents = [faq.intent for faq in faqs]
                
                # Create TF-IDF vectorizer
                self.vectorizer = TfidfVectorizer(
                    max_features=1000,
                    stop_words='english',
                    ngram_range=(1, 2)
                )
                
                # Transform questions to vectors
                X = self.vectorizer.fit_transform(questions)
                
                # Train Naive Bayes classifier
                self.classifier = MultinomialNB()
                self.classifier.fit(X, intents)
                
        except Exception as e:
            print(f"Error loading NLU model: {e}")
            self.vectorizer = None
            self.classifier = None
    
    def _detect_intent(self, message):
        """Detect intent from user message"""
        if not self.vectorizer or not self.classifier:
            return None, 0.0
        
        try:
            # Transform user message
            message_vector = self.vectorizer.transform([message])
            
            # Predict intent
            intent = self.classifier.predict(message_vector)[0]
            
            # Get confidence score
            confidence = np.max(self.classifier.predict_proba(message_vector))
            
            return intent, confidence
        except Exception as e:
            print(f"Error detecting intent: {e}")
            return None, 0.0
    
    def _extract_entities(self, message):
        """Extract entities from user message"""
        entities = {}
        
        # Extract amount
        amount_pattern = r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)'
        amount_match = re.search(amount_pattern, message)
        if amount_match:
            entities['amount'] = float(amount_match.group(1).replace(',', ''))
        
        # Extract account number
        account_pattern = r'\b(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})\b'
        account_match = re.search(account_pattern, message)
        if account_match:
            entities['account_number'] = account_match.group(1)
        
        # Extract date
        date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b'
        date_match = re.search(date_pattern, message)
        if date_match:
            entities['date'] = date_match.group(1)
        
        return entities
    
    def _generate_response(self, intent, entities, user):
        """Generate response based on detected intent and entities"""
        if intent == 'check_balance':
            if user.is_authenticated:
                # Get user's account balance
                from banking.models import Account
                accounts = Account.objects.filter(user=user, is_active=True)
                if accounts.exists():
                    total_balance = sum(account.balance for account in accounts)
                    return f"Your total balance across all accounts is ${total_balance:,.2f}"
                else:
                    return "You don't have any active accounts."
            else:
                return "Please log in to check your balance."
        
        elif intent == 'transfer_money':
            if 'amount' in entities and 'account_number' in entities:
                return f"I can help you transfer ${entities['amount']:,.2f} to account {entities['account_number']}. Please use the transfer form in your banking portal."
            else:
                return "To transfer money, please provide the amount and destination account number."
        
        elif intent == 'transaction_history':
            if user.is_authenticated:
                return "I can show you your recent transactions. Please check the transactions tab in your banking portal."
            else:
                return "Please log in to view your transaction history."
        
        elif intent == 'account_info':
            if user.is_authenticated:
                from banking.models import Account
                accounts = Account.objects.filter(user=user, is_active=True)
                if accounts.exists():
                    account_info = []
                    for account in accounts:
                        account_info.append(f"{account.account_type.title()}: {account.account_number} - ${account.balance:,.2f}")
                    return "Your accounts:\n" + "\n".join(account_info)
                else:
                    return "You don't have any active accounts."
            else:
                return "Please log in to view your account information."
        
        else:
            # Try to find FAQ answer
            try:
                faq = BankingFAQ.objects.filter(intent=intent).first()
                if faq:
                    return faq.answer
            except:
                pass
            
            return "I'm sorry, I didn't understand your request. How can I help you with your banking needs?"
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Handle chat messages and generate responses"""
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            session_id = serializer.validated_data.get('session_id', str(uuid.uuid4()))
            
            # Get or create conversation
            conversation, created = Conversation.objects.get_or_create(
                user=request.user,
                session_id=session_id
            )
            
            # Save user message
            user_message = Message.objects.create(
                conversation=conversation,
                message_type='user',
                content=message
            )
            
            # Detect intent
            intent, confidence = self._detect_intent(message)
            
            # Extract entities
            entities = self._extract_entities(message)
            
            # Generate response
            response = self._generate_response(intent, entities, request.user)
            
            # Save bot response
            bot_message = Message.objects.create(
                conversation=conversation,
                message_type='bot',
                content=response,
                intent_detected=intent or '',
                confidence_score=confidence,
                entities_extracted=entities
            )
            
            # Update conversation timestamp
            conversation.save()
            
            # Prepare response data
            response_data = {
                'response': response,
                'intent_detected': intent or '',
                'confidence_score': confidence,
                'entities': entities,
                'session_id': session_id,
                'suggested_actions': self._get_suggested_actions(intent)
            }
            
            return Response(response_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_suggested_actions(self, intent):
        """Get suggested actions based on detected intent"""
        suggestions = {
            'check_balance': ['View detailed balance', 'Check other accounts'],
            'transfer_money': ['Complete transfer', 'View transfer history'],
            'transaction_history': ['Download statement', 'Filter transactions'],
            'account_info': ['Update account details', 'Open new account']
        }
        return suggestions.get(intent, ['Ask another question', 'Get help'])
    
    @action(detail=False, methods=['post'])
    def train(self, request):
        """Train the chatbot with new data"""
        serializer = TrainingDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                questions = serializer.validated_data['questions']
                answers = serializer.validated_data['answers']
                intent = serializer.validated_data['intent']
                category = serializer.validated_data['category']
                
                # Create FAQ entries
                for question, answer in zip(questions, answers):
                    BankingFAQ.objects.create(
                        question=question,
                        answer=answer,
                        intent=intent,
                        category=category,
                        confidence_score=0.8
                    )
                
                # Retrain the model
                self._load_nlu_model()
                
                return Response({'message': 'Training completed successfully'})
                
            except Exception as e:
                return Response(
                    {'error': f'Training failed: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def intents(self, request):
        """Get available intents"""
        intents = Intent.objects.all()
        serializer = IntentSerializer(intents, many=True)
        return Response(serializer.data)
