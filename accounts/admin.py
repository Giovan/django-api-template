from django.contrib import admin

from .models import (User, SingleQrCode, Session,
UserSignup, UserLogin, Newsletter, Blacklist)

admin.site.register([User, SingleQrCode, Session,
UserSignup, UserLogin, Newsletter, Blacklist])
