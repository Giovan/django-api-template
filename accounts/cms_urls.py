# accounts/cms_urls.py

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .accounts_views import UsersList, UsersCreate,\
UsersDetail, UsersUpdate, UsersDelete


urlpatterns = [
    path('users', csrf_exempt(UsersList.as_view())),
    path('users/<int:pk>', csrf_exempt(UsersDetail.as_view())),
    path('users-create', csrf_exempt(UsersCreate.as_view())),
    path('users-update/<int:pk>', csrf_exempt(UsersUpdate.as_view())),
    path('users-delete/<int:pk>', csrf_exempt(UsersDelete.as_view())),
]
