# accounts/urls.py
from django.urls import path

from .views import UserDetailView, UserPresignedUrlsView, UserPresignedAvatarUrlsView

urlpatterns = [
    path('account/', UserDetailView.as_view()),
    # path('presigned-urls/', UserPresignedUrlsView.as_view()),
    # path('presigned-avatar-url/', UserPresignedAvatarUrlsView.as_view()),
]
