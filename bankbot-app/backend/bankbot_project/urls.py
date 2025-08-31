"""
URL configuration for bankbot_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
import json

def home_view(request):
    return JsonResponse({
        'message': 'BankBot API is running!',
        'endpoints': {
            'admin': '/admin/',
            'banking_api': '/api/banking/',
            'chatbot_api': '/api/chatbot/',
            'auth_login': '/api/auth/login/',
            'auth_logout': '/api/auth/logout/',
            'auth_register': '/api/auth/register/'
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
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return JsonResponse({
                'error': 'Invalid credentials'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
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
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'error': 'Username already exists'
            }, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'error': 'Email already exists'
            }, status=400)
        
        # Create new user
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
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/banking/', include('banking.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/register/', register_view, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
