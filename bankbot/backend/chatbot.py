"""
Perfect AI Chatbot Module for BankBot
Intelligent banking assistance with learning capabilities
"""

import re
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

class BankBot:
    """Advanced AI Banking Assistant with intelligent responses"""
    
    def __init__(self):
        """Initialize BankBot with comprehensive knowledge base"""
        self.knowledge_base = {
            "balance": {
                "patterns": [
                    r"\b(balance|how much|money|account.*balance|check.*balance|what.*balance|current.*balance|total.*balance)\b",
                    r"\b(how.*much.*have|what.*in.*account|show.*balance|display.*balance)\b",
                    r"\b(account.*total|funds.*available|available.*funds|current.*funds)\b"
                ],
                "responses": [
                    "Your current balance is ${balance}. You have {accounts} account(s) with us.",
                    "Based on your accounts, your total balance is ${balance}.",
                    "You currently have ${balance} across all your accounts.",
                    "Your total available balance is ${balance}.",
                    "As of now, your balance is ${balance} across {accounts} account(s)."
                ],
                "priority": 10
            },
            "transfer": {
                "patterns": [
                    r"\b(transfer|send.*money|move.*money|payment|how.*transfer|transfer.*money|send.*payment)\b",
                    r"\b(wire.*transfer|bank.*transfer|online.*transfer|mobile.*transfer)\b",
                    r"\b(transfer.*between|move.*funds|send.*funds|pay.*someone)\b"
                ],
                "responses": [
                    "To transfer money, you can use the Transfer tab in your dashboard. You can transfer between your accounts or to external accounts.",
                    "Money transfers can be done through the banking portal. You'll need the recipient's account number and routing number.",
                    "You can transfer funds using the mobile app or online banking. Transfers between your accounts are instant.",
                    "For transfers, visit the Transfer section where you can send money to other accounts or between your own accounts.",
                    "Transfer money easily through our secure portal. Internal transfers are instant, external transfers typically take 1-3 business days."
                ],
                "priority": 9
            },
            "transactions": {
                "patterns": [
                    r"\b(transaction|history|recent.*activity|statement|what.*spent|where.*money|payment.*history)\b",
                    r"\b(spending.*history|expense.*tracking|income.*tracking|financial.*activity)\b",
                    r"\b(monthly.*statement|account.*activity|transaction.*log|payment.*record)\b"
                ],
                "responses": [
                    "Your recent transactions are available in the Transactions tab. You can filter by date, amount, or category.",
                    "You can view your transaction history in the dashboard. This includes all deposits, withdrawals, and transfers.",
                    "Transaction history is updated in real-time. You can download statements or view them online.",
                    "Check the Transactions section to see your recent activity, spending patterns, and income sources.",
                    "Your financial activity is tracked in real-time. View detailed transaction history with categorization and filtering options."
                ],
                "priority": 8
            },
            "account": {
                "patterns": [
                    r"\b(account|account.*info|account.*details|my.*account|account.*number|account.*type|how.*account)\b",
                    r"\b(account.*information|account.*summary|account.*overview|account.*status)\b",
                    r"\b(routing.*number|account.*details|account.*settings|account.*preferences)\b"
                ],
                "responses": [
                    "You have {accounts} account(s) with us. Your main account is a checking account with account number ending in ****.",
                    "Your account information is displayed in the Accounts tab. You can view balances, account numbers, and account types.",
                    "Account details including routing numbers and account numbers are available in your account settings.",
                    "View your account summary in the Accounts section. Each account shows its type, number, and current balance.",
                    "Your accounts are listed in the dashboard with detailed information including account numbers and types."
                ],
                "priority": 7
            },
            "help": {
                "patterns": [
                    r"\b(help|support|assist|what.*can.*do|how.*help|guide|tutorial|instructions)\b",
                    r"\b(how.*use|how.*work|what.*features|banking.*help|customer.*support)\b",
                    r"\b(help.*menu|support.*options|assistance|guidance|walkthrough)\b"
                ],
                "responses": [
                    "I can help you with balance inquiries, transfers, transaction history, account information, and general banking questions.",
                    "I'm here to assist with your banking needs. You can ask me about balances, transfers, transactions, or account details.",
                    "I'm your AI banking assistant. I can help you navigate your accounts, understand transactions, and perform banking tasks.",
                    "I can assist with account management, financial tracking, transfers, and general banking inquiries. What would you like to know?",
                    "I'm here to help! I can provide information about your accounts, transactions, transfers, and answer banking questions."
                ],
                "priority": 6
            },
            "security": {
                "patterns": [
                    r"\b(security|safe|secure|protected|encryption|authentication|password|login)\b",
                    r"\b(two.*factor|2fa|multi.*factor|biometric|fingerprint|face.*id)\b",
                    r"\b(account.*security|fraud.*protection|identity.*theft|scam|phishing)\b"
                ],
                "responses": [
                    "Your account is protected with bank-grade security including 256-bit encryption, two-factor authentication, and fraud monitoring.",
                    "We use enterprise-level security measures including SSL encryption, secure authentication, and 24/7 fraud detection.",
                    "Your security is our priority. We employ multiple layers of protection including encryption, authentication, and monitoring.",
                    "Rest assured, your account is secured with industry-standard encryption, secure login, and comprehensive fraud protection.",
                    "Security features include encrypted connections, secure authentication, fraud alerts, and account monitoring systems."
                ],
                "priority": 5
            },
            "fees": {
                "patterns": [
                    r"\b(fees|charges|costs|monthly.*fee|maintenance.*fee|overdraft|penalty)\b",
                    r"\b(account.*fees|service.*charges|transaction.*fees|atm.*fees)\b",
                    r"\b(no.*fees|free.*banking|fee.*waiver|minimum.*balance)\b"
                ],
                "responses": [
                    "We offer transparent fee structures. Most accounts have no monthly maintenance fees when you maintain a minimum balance.",
                    "Our fee schedule is clearly outlined in your account agreement. Many services are free with qualifying account balances.",
                    "Fees vary by account type and services used. Check your account terms for specific fee information.",
                    "We strive to keep fees minimal. Most basic banking services are free with qualifying account balances.",
                    "Fee information is available in your account documents. Contact us for specific fee questions about your account."
                ],
                "priority": 4
            }
        }
        
        self.fallback_responses = [
            "I'm here to help with your banking needs. Could you please rephrase your question?",
            "I didn't quite understand that. You can ask me about your balance, transfers, transactions, or account information.",
            "I'm still learning! Try asking about your balance, transfers, or account information.",
            "I'm not sure I understood. Could you try asking about your accounts, transactions, or banking services?",
            "I'd be happy to help with banking questions. Try asking about balances, transfers, or account details."
        ]
        
        self.suggested_actions = {
            "balance": ["View detailed balance", "Check other accounts", "Download statement", "Set up alerts"],
            "transfer": ["Complete transfer", "View transfer history", "Set up recurring transfers", "Manage beneficiaries"],
            "transactions": ["Download statement", "Filter transactions", "Export data", "Set up categories"],
            "account": ["Update account details", "Open new account", "Change account settings", "View statements"],
            "help": ["Browse help center", "Contact support", "Schedule appointment", "View tutorials"],
            "security": ["Update password", "Enable 2FA", "Review security settings", "Set up alerts"],
            "fees": ["View fee schedule", "Check account terms", "Contact support", "Review services"]
        }
        
        # Learning and improvement
        self.conversation_history = defaultdict(list)
        self.response_feedback = defaultdict(list)
        self.intent_confidence = defaultdict(float)
        
    def get_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get intelligent response based on user message and context"""
        message_lower = message.lower().strip()
        
        # Store conversation for learning
        session_id = user_context.get("session_id", "default")
        self.conversation_history[session_id].append({
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "user_context": user_context
        })
        
        # Detect intent with confidence scoring
        intent_result = self._detect_intent_with_confidence(message_lower)
        intent = intent_result["intent"]
        confidence = intent_result["confidence"]
        
        # Generate contextual response
        if intent and confidence > 0.3:
            response = self._generate_response(intent, user_context)
            # Update confidence based on pattern matching
            self.intent_confidence[intent] = min(1.0, self.intent_confidence[intent] + 0.1)
        else:
            response = self._get_fallback_response()
            intent = "general"
            confidence = 0.2
        
        # Get suggested actions
        suggested_actions = self.suggested_actions.get(intent, ["Ask another question", "Get help"])
        
        # Store response for learning
        self.conversation_history[session_id].append({
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "message": response,
            "intent": intent,
            "confidence": confidence,
            "suggested_actions": suggested_actions,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        }
    
    def _detect_intent_with_confidence(self, message: str) -> Dict[str, Any]:
        """Detect user intent with confidence scoring"""
        best_intent = None
        best_confidence = 0.0
        matched_patterns = []
        
        for intent, data in self.knowledge_base.items():
            intent_confidence = 0.0
            pattern_matches = 0
            
            for pattern in data["patterns"]:
                if re.search(pattern, message, re.IGNORECASE):
                    pattern_matches += 1
                    # Higher confidence for longer, more specific patterns
                    pattern_confidence = min(1.0, len(pattern) / 50.0)
                    intent_confidence = max(intent_confidence, pattern_confidence)
            
            if pattern_matches > 0:
                # Boost confidence based on priority and pattern matches
                priority_boost = data.get("priority", 5) / 10.0
                match_boost = min(0.3, pattern_matches * 0.1)
                total_confidence = intent_confidence + priority_boost + match_boost
                
                if total_confidence > best_confidence:
                    best_confidence = total_confidence
                    best_intent = intent
                    matched_patterns = pattern_matches
        
        return {
            "intent": best_intent,
            "confidence": min(1.0, best_confidence),
            "pattern_matches": matched_patterns
        }
    
    def _generate_response(self, intent: str, user_context: Dict[str, Any]) -> str:
        """Generate contextual response based on intent and user context"""
        responses = self.knowledge_base[intent]["responses"]
        
        # Select response (could be improved with ML in the future)
        response = random.choice(responses)
        
        # Personalize response with user context
        if intent == "balance":
            balance = user_context.get('balance', 0)
            accounts = user_context.get('accounts', 1)
            response = response.replace("{balance}", f"{balance:,.2f}")
            response = response.replace("{accounts}", str(accounts))
            
            # Add personalized insights
            if balance > 10000:
                response += " Great job maintaining a healthy balance!"
            elif balance < 1000:
                response += " Consider setting up automatic savings to build your balance."
                
        elif intent == "account":
            accounts = user_context.get('accounts', 1)
            response = response.replace("{accounts}", str(accounts))
            
            # Add account-specific insights
            if accounts > 2:
                response += " You have a well-diversified account structure!"
            elif accounts == 1:
                response += " Consider opening a savings account to start building your emergency fund."
        
        return response
    
    def _get_fallback_response(self) -> str:
        """Get fallback response when intent is not detected"""
        return random.choice(self.fallback_responses)
    
    def learn_from_feedback(self, session_id: str, feedback: bool, message: str = None):
        """Learn from user feedback to improve responses"""
        if session_id in self.conversation_history:
            self.response_feedback[session_id].append({
                "feedback": feedback,
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_suggested_questions(self) -> List[str]:
        """Get suggested questions for users"""
        return [
            "What's my current balance?",
            "How do I transfer money?",
            "Show my recent transactions",
            "Tell me about my accounts",
            "What are your banking hours?",
            "How secure is my account?",
            "What fees do you charge?",
            "How do I set up alerts?"
        ]
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of conversation for a session"""
        if session_id not in self.conversation_history:
            return {"error": "Session not found"}
        
        conversation = self.conversation_history[session_id]
        intents = [msg.get("intent") for msg in conversation if msg.get("intent")]
        
        return {
            "session_id": session_id,
            "message_count": len([msg for msg in conversation if "message" in msg]),
            "response_count": len([msg for msg in conversation if "response" in msg]),
            "intents_discussed": list(set(intents)),
            "session_duration": self._calculate_session_duration(conversation),
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_session_duration(self, conversation: List[Dict]) -> str:
        """Calculate the duration of a conversation session"""
        if len(conversation) < 2:
            return "0 minutes"
        
        first_msg = conversation[0].get("timestamp")
        last_msg = conversation[-1].get("timestamp")
        
        try:
            start_time = datetime.fromisoformat(first_msg)
            end_time = datetime.fromisoformat(last_msg)
            duration = end_time - start_time
            minutes = duration.total_seconds() / 60
            
            if minutes < 1:
                return "Less than 1 minute"
            elif minutes < 60:
                return f"{int(minutes)} minutes"
            else:
                hours = minutes / 60
                return f"{hours:.1f} hours"
        except:
            return "Unknown duration"