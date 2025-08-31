"""
URL configuration for bankbot_project project.
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({
        'message': 'BankBot API is running!',
        'status': 'success',
        'version': '1.0.0'
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
]
