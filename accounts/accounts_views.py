from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.permissions import BlacklistPermission

from .models import User
from .serializers import UsersCMSDetailSerializer


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCMSDetailSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated, BlacklistPermission]


class UsersCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCMSDetailSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated, BlacklistPermission]


class UsersDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCMSDetailSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated, BlacklistPermission]


class UsersUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCMSDetailSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated, BlacklistPermission]


class UsersDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCMSDetailSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated, BlacklistPermission]
