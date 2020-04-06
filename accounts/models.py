from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from datetime import datetime
from pgcrypto import fields
from uuid import uuid4

# from plan.models import Plan


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email: str, password: str,
        is_staff: bool, is_superuser: bool, **kwargs):
        email = self.normalize_email(email)
        activation_code = uuid.uuid1()
        reference_code = str(str(uuid.uuid1()).split("-")[0])
        user_has_code = User.objects.filter(reference=reference_code).first()
        if not user_has_code:
            user = self.model(
                email=email,
                is_active=True,
                is_staff=False,
                is_superuser=False,
                activation_code=activation_code,
                reference=reference_code,
                **kwargs
            )
            user.set_password(password)
            user.save(using=self._db)

        return user, activation_code

    def create_user(self, email: str, password: str, **extra_fields):
        user_created, activation_code = self._create_user(
            email=email,
            password=password,
            **extra_fields
        ) 
        if user_created:
            self.send_mail(email, activation_code)

        return user_created

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self._create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )


class User(PermissionsMixin, AbstractBaseUser):
    digest_field = fields.TextDigestField(blank=True, default='')
    digest_with_original_field = fields.TextDigestField(original='', default='')
    hmac_field = fields.TextHMACField(blank=True, default='')
    hmac_with_original_field = fields.TextHMACField(original='', default='')
    varopago_id = fields.TextPGPSymmetricKeyField(editable=False, blank=False, default='-')
    username = fields.CharPGPSymmetricKeyField(max_length=255, blank=False, null=False, unique=True, default='')
    name = fields.CharPGPSymmetricKeyField(max_length=200, blank=False, null=False, default='')
    second_name = fields.CharPGPSymmetricKeyField(max_length=200, blank=False, null=False, default='')
    first_lastname = fields.CharPGPSymmetricKeyField(max_length=250, blank=True, null=True, default='')
    second_lastname = fields.CharPGPSymmetricKeyField(max_length=250, blank=True, null=True, default='')
    country = fields.CharPGPSymmetricKeyField(max_length=250, blank=True, null=True, default='')
    email = fields.EmailPGPSymmetricKeyField(unique=True)
    phone = fields.CharPGPSymmetricKeyField(max_length=200, blank=False, null=False, default='')
    rol = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    avatar = fields.TextPGPSymmetricKeyField(blank=True, null=True, default='')
    banner = fields.TextPGPSymmetricKeyField(blank=True, null=True, default='')
    plan = models.ForeignKey(Plan, related_name='user_plan', null=True, blank=True,
                             on_delete=models.SET_NULL)
    plan_payment = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, null=True, editable=True)
    plan_paid_lenght = fields.IntegerPGPSymmetricKeyField(blank=True, null=True, default=0)
    plan_expiration = fields.DatePGPSymmetricKeyField(blank=True, null=True)
    invitation_code = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    is_staff_varopago = fields.IntegerPGPSymmetricKeyField(blank=True, null=True, default=0)
    is_staff_dev = fields.IntegerPGPSymmetricKeyField(blank=True, null=True, default=0)
    is_active_user = fields.IntegerPGPSymmetricKeyField(blank=True, null=True, default=1)
    date_joined = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=now, blank=False, editable=False)
    address = fields.TextPGPSymmetricKeyField(blank=False, default='')
    activation_code = fields.TextPGPSymmetricKeyField(blank=False, default='')
    kyc = JSONField(default=dict)
    previous_reference = fields.TextPGPSymmetricKeyField(blank=False, default='')
    reference = fields.TextPGPSymmetricKeyField(blank=False, default='')

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    class Meta:
        app_label = 'accounts'

    USERNAME_FIELD = 'email'


class SingleQrCode(models.Model):
    token = fields.TextDigestField(blank=True, default=uuid4, editable=False)
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    image_name = fields.TextDigestField(blank=True, default='')
    url_image = fields.TextDigestField(blank=True, default='')
    type_qr = fields.TextDigestField(blank=True, default='')
    latitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True, default=0.00000)
    longitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True, default=0.00000)
    created = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=False)
    last_status_change = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'accounts'


class Session(models.Model):
    session_token = fields.TextDigestField(blank=True, default='')
    session_profile = fields.CharPGPSymmetricKeyField(max_length=50, blank=True, null=True, default='')
    session_ip = fields.CharPGPSymmetricKeyField(max_length=50, blank=True, null=True, default='')
    session_setted_at = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=False)
    session_finished_at = fields.DateTimePGPSymmetricKeyField(default='', blank=True, null=True, editable=True)
    user_session = models.ForeignKey(User, null=True, blank=False, related_name="user_session", on_delete=models.SET_NULL)
    created = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=False)
    last_status_change = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        app_label = 'accounts'


class UserSignup(models.Model):
    email = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    anonymous_ip = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    app_ip = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    webapp_ip = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    dev_api_ip = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    device = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    created = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=False)
    last_status_change = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        app_label = 'accounts'


class UserLogin(models.Model):
    email = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    ip = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    device = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    try_of_login = fields.CharPGPSymmetricKeyField(max_length=255, blank=True, null=True, default='')
    created = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=False)
    last_status_change = fields.DateTimePGPSymmetricKeyField(default=now, blank=True, editable=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        app_label = 'accounts'


class Blacklist(models.Model):
    ip_addr = models.GenericIPAddressField()


    class Meta:
        app_label = 'accounts'
