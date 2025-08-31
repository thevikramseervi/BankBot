"""
BankBot AI Assistant - Intelligent Banking Chatbot
"""

import re
from typing import Dict, List, Any
from datetime import datetime

class BankBot:
    def __init__(self):
        """Initialize BankBot with knowledge base and patterns"""
        self.knowledge_base = {
            "balance": {
                "patterns": [
                    r"balance", r"how much", r"money", r"account.*balance",
                    r"check.*balance", r"what.*balance", r"current.*balance"
                ],
                "responses": [
                    "Your current balance is ${balance}. You have {accounts} account(s).",
                    "Based on your accounts, your total balance is ${balance}.",
                    "You currently have ${balance} across all your accounts."
                ]
            },
            "transfer": {
                "patterns": [
                    r"transfer", r"send.*money", r"move.*money", r"payment",
                    r"how.*transfer", r"transfer.*money", r"send.*payment"
                ],
                "responses": [
                    "To transfer money, you can use the Transfer tab in your dashboard. You can transfer between your accounts or to external accounts.",
                    "Money transfers can be done through the banking portal. You'll need the recipient's account number and routing number.",
                    "You can transfer funds using the mobile app or online banking. Transfers between your accounts are instant."
                ]
            },
            "transactions": {
                "patterns": [
                    r"transaction", r"history", r"recent.*activity", r"statement",
                    r"what.*spent", r"where.*money", r"payment.*history"
                ],
                "responses": [
                    "Your recent transactions are available in the Transactions tab. You can filter by date, amount, or category.",
                    "You can view your transaction history in the dashboard. This includes all deposits, withdrawals, and transfers.",
                    "Transaction history is updated in real-time. You can download statements or view them online."
                ]
            },
            "account": {
                "patterns": [
                    r"account", r"account.*info", r"account.*details", r"my.*account",
                    r"account.*number", r"account.*type", r"how.*account"
                ],
                "responses": [
                    "You have {accounts} account(s) with us. Your main account is a checking account with account number ending in ****.",
                    "Your account information is displayed in the Accounts tab. You can view balances, account numbers, and account types.",
                    "Account details including routing numbers and account numbers are available in your account settings."
                ]
            },
            "help": {
                "patterns": [
                    r"help", r"support", r"assist", r"what.*can.*do", r"how.*help",
                    r"guide", r"tutorial", r"instructions"
                ],
                "responses": [
                    "I can help you with balance inquiries, transfers, transaction history, account information, and general banking questions.",
                    "I'm here to assist with your banking needs. You can ask me about balances, transfers, transactions, or account details.",
                    "I'm your AI banking assistant. I can help you navigate your accounts, understand transactions, and perform banking tasks."
                ]
            }
        }
        
        self.fallback_responses = [
            "I'm here to help with your banking needs. Could you please rephrase your question?",
            "I didn't quite understand that. You can ask me about your balance, transfers, transactions, or account information.",
            "I'm still learning! Try asking about your balance, transfers, or account information."
        ]
        
        self.suggested_actions = {
            "balance": ["View detailed balance", "Check other accounts", "Download statement"],
            "transfer": ["Complete transfer", "View transfer history", "Set up recurring transfers"],
            "transactions": ["Download statement", "Filter transactions", "Export data"],
            "account": ["Update account details", "Open new account", "Change account settings"],
            "help": ["Browse help center", "Contact support", "Schedule appointment"]
        }

    def get_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get intelligent response based on user message and context"""
        message_lower = message.lower()
        
        # Detect intent
        intent = self._detect_intent(message_lower)
        
        # Generate response
        if intent:
            response = self._generate_response(intent, user_context)
            confidence = 0.9
        else:
            response = self._get_fallback_response()
            intent = "general"
            confidence = 0.3
        
        # Get suggested actions
        suggested_actions = self.suggested_actions.get(intent, ["Ask another question", "Get help"])
        
        return {
            "message": response,
            "intent": intent,
            "confidence": confidence,
            "suggested_actions": suggested_actions,
            "timestamp": datetime.now().isoformat()
        }

    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent
        return None

    def _generate_response(self, intent: str, user_context: Dict[str, Any]) -> str:
        """Generate contextual response based on intent and user context"""
        responses = self.knowledge_base[intent]["responses"]
        
        # Select response and personalize it
        response = responses[0]  # For now, use first response
        
        # Personalize response with user context
        if intent == "balance":
            response = response.replace("{balance}", f"{user_context.get('balance', 0):,.2f}")
            response = response.replace("{accounts}", str(user_context.get('accounts', 1)))
        elif intent == "account":
            response = response.replace("{accounts}", str(user_context.get('accounts', 1)))
        
        return response

    def _get_fallback_response(self) -> str:
        """Get fallback response when intent is not detected"""
        import random
        return random.choice(self.fallback_responses)