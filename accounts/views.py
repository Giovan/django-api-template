import os
import datetime, uuid, pyqrcode, boto3, botocore
from django.conf import settings

# Let's use Amazon S3
# Do not hard code credentials
"""
s3_con = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)
"""

from babel.numbers import format_number, format_decimal, format_currency

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.permissions import BlacklistPermission, IsUserOwner

from .models import User, SingleQrCode, Newsletter
from .serializers import (
    SignUpUserSerializer,
    SingleQrCodeSerializer,
    TokenSerializer,
    UserDetailSerializer,
    UserReferenceSerializer
)

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SignUpView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    
    @classmethod
    def get_extra_actions(cls):
        return []

    @staticmethod
    def post(request):
# Get the IP of the request
# user_signup = UserSignup.objects.create(email='mail@gmail.com', ip='-', device='-')
        serializer = SignUpUserSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        if serializer.is_valid():
            user = serializer.save()
            if user:
                qr_code = SingleQrCode.objects.create(
                    user=user,
                    image_name='',
                    url_image='',
                    type_qr='user_account',
                    latitude=0.0000000,
                    longitude=0.0000000
                )
                if qr_code:
                    token_user_generated = qr_code.token
                    image_name = str(token_user_generated) + '.png'
                    """
                    qr_code_generated = pyqrcode.create(str(token_user_generated), error='L')
                    qr_code_generated.png(settings.MEDIA_ROOT+'/'+str(token_user_generated) + '.png', scale=12, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
                    data = open(settings.MEDIA_ROOT+'/'+str(token_user_generated) + '.png', 'rb+')

                    # Create an S3 client
                    s3_resource = boto3.resource('s3')
                    s3_resource.Object('', 'qrcodes').upload_file(Filename=image_name)

                    # Uploads the given file using a managed uploader, which will split up large
                    # files automatically and upload parts in parallel.
                    s3.upload_file(filename, bucket_name, filename)
                    SingleQrCode.objects.filter(token=qr_code.token).update(image_name=image_name, url_image=url_image)
                    """
                    # Newsletter.objects.create(newsletter=True, user_news=user)
                    folder = settings.MEDIA_ROOT+'/'
                    file_path = str(token_user_generated) + '.png'
                    file_path = os.path.join(folder, file_path)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        os.unlink(file_path)
                        print(e)
            return Response(
                {},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


#Login view
class LoginView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,) 

    @staticmethod
    def post(request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        user = User.objects.filter(email=email, is_active=True).first()
        if user is not None:
            user_logged = user.check_password(password)
        if user_logged:
            # Logins saves the user´s ID in the session,
            # using Django´s session framework.
            login(request, user)
        serializer = TokenSerializer(data={
            # using DRF JWT utility functions to generate a token
            "token": jwt_encode_handler(
                jwt_payload_handler(user)
            )}
        )
        response_data = {
            "user_token": serializer.initial_data['token']
        }
        if serializer.is_valid():
            return Response(
                data=response_data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDetailView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOwner, BlacklistPermission]

    @staticmethod
    def get(request):
        data_response = { 
            'user_data': UserDetailSerializer(
                request.user
            ).data
        }
        return Response(
            data=data_response,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def patch(request):
        updated_user = UserDetailSerializer().update(
            request.user,
            request.data
        )
        updated_user.save()
        data_response = { 
            'user_data': UserDetailSerializer(
                updated_user
            ).data
        }
        return Response(
            data=data_response,
            status=status.HTTP_200_OK
        )


"""
class UserPresignedUrlsView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOwner, BlacklistPermission]

    @staticmethod
    def get(request):
        requested_urls = request.data.get("requested_urls", "")
        # get user email or ID
        urls_finale = {}
        for element in requested_urls:
            url = s3_con.generate_presigned_url(
                    'put_object',
                    Params={
                        'Bucket': settings.AWS_S3_BUCKET,
                        'Key': element,
                        'ContentType':'image/jpg'
                    },
                    ExpiresIn=600,
                    HttpMethod='PUT'
                )
            # save the custom url in the database to link with the user requested account
            if element not in urls_finale:
                urls_finale[element] = url
        data_response = { 
            'signed_urls': urls_finale
        }
        return Response(
            data=data_response,
            status=status.HTTP_200_OK
        )


class UserPresignedAvatarUrlsView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOwner, BlacklistPermission]

    @staticmethod
    def get(request):
        urls_finale = {}
        data_response = { 
            'signed_url': urls_finale
        }
        return Response(
            data=data_response,
            status=status.HTTP_200_OK
        )
"""
