"""api URL Configuration
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

urlpatterns = [
# Main Page route
    path('', admin.site.urls),
# Django admin routes
    path('admin/', admin.site.urls),   
# Auth routes
# path('auth/', include('accounts.auth_urls')),
    path('api-token-refresh/', refresh_jwt_token, name='refresh-token'),
    path('api-token-verify/', verify_jwt_token, name='verify-token'),
]
