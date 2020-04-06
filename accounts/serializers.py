from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User, SingleQrCode
# from plan.models import Plan


class SignUpUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255, required=False, default='')
    password = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255, required=False, default='')
    address = serializers.CharField(max_length=255, required=False, default='')
    invitation_code = serializers.CharField(max_length=255, required=False, default='')

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['first_name'],
            first_lastname = validated_data['last_name'],
            rol = 'user',
            password = validated_data['password'],
            country = validated_data['country'],
            phone = validated_data['phone'],
            invitation_code = validated_data['invitation_code'],
            is_active_user = True
        )
        return user

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_email(email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                'This email has already been linked to an existing account'
            )

        return email

    @staticmethod
    def validate_password(password):
        validate_password(password)
    
        return password


# SingleQrCode Serializer
class SingleQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleQrCode
        fields = '__all__'


# Login Serializer
class LoginSerializer(serializers.Serializer):
    """
    This serializer serializes the login data
    """
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


# Token Serializer
class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


# UsersCMSDetail Serializer
class UsersCMSDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'varopago_id',
            'username',
            'name',
            'second_name',
            'first_lastname',
            'second_lastname',
            'country',
            'email',
            'phone',
            'rol',
            'avatar',
            'banner',
            'plan',
            'invitation_code',
            'is_staff_varopago',
            'is_staff_dev',
            'is_active_user',
            'date_joined',
            'is_active',
            'is_staff',
            'address',
            'activation_code',
            'kyc',
            'previous_reference',
            'reference'
        )


# UserDetail Serializer
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'second_name',
            'first_lastname',
            'second_lastname',
            'country',
            'email',
            'phone',
            'rol',
            'avatar',
            'plan',
            'invitation_code',
            'address',
        )
        read_only_fields = (
            'email',
            'name',
            'first_lastname',
        )


class UserReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'reference',
            'previous_reference'
        )
