"""
URL configuration for simple_bankbot project.
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
import json

def home_view(request):
    return JsonResponse({
        'message': 'BankBot API is running!',
        'status': 'success',
        'version': '2.0.0',
        'endpoints': {
            'admin': '/admin/',
            'auth_login': '/api/auth/login/',
            'auth_logout': '/api/auth/logout/',
            'auth_register': '/api/auth/register/',
            'chat': '/api/chat/',
            'balance': '/api/balance/',
            'transactions': '/api/transactions/'
        }
    })

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                'error': 'Username and password are required'
            }, status=400)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return JsonResponse({
                'error': 'Invalid credentials'
            }, status=401)
            
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    try:
        logout(request)
        return JsonResponse({
            'message': 'Logout successful'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return JsonResponse({
                'error': 'Username, email, and password are required'
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'error': 'Username already exists'
            }, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def chat_view(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').lower()
        
        # Simple chatbot logic
        if 'balance' in message:
            response = "Your current balance is $2,450.67. You can view detailed account information in your dashboard."
        elif 'transfer' in message:
            response = "To transfer money, go to the Transfers tab in your dashboard. You can transfer between your accounts or to other bank accounts."
        elif 'transaction' in message:
            response = "Your recent transactions are displayed in the Transactions tab. You can filter by date, amount, or type."
        elif 'account' in message:
            response = "You have a checking account (****1234) with $1,234.56 and a savings account (****5678) with $1,216.11."
        elif 'help' in message:
            response = "I can help you with balance inquiries, transfers, transaction history, and account information. What would you like to know?"
        else:
            response = "I'm here to help with your banking needs. You can ask me about your balance, transfers, transactions, or account information."
        
        return JsonResponse({
            'response': response,
            'intent_detected': 'banking_assistance',
            'confidence_score': 0.9
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
def balance_view(request):
    return JsonResponse({
        'checking': 1234.56,
        'savings': 1216.11,
        'total': 2450.67,
        'currency': 'USD'
    })

@csrf_exempt
def transactions_view(request):
    return JsonResponse({
        'transactions': [
            {
                'id': 1,
                'type': 'debit',
                'amount': -45.67,
                'description': 'Coffee Shop',
                'date': '2024-01-15',
                'balance': 1234.56
            },
            {
                'id': 2,
                'type': 'credit',
                'amount': 2500.00,
                'description': 'Salary Deposit',
                'date': '2024-01-14',
                'balance': 1280.23
            }
        ]
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/register/', register_view, name='register'),
    path('api/chat/', chat_view, name='chat'),
    path('api/balance/', balance_view, name='balance'),
    path('api/transactions/', transactions_view, name='transactions'),
]
