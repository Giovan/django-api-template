# accounts/auth_urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (SignUpView, LoginView)

urlpatterns = [
    path('signup', csrf_exempt(SignUpView.as_view())),
    path('login', csrf_exempt(LoginView.as_view())),
]
