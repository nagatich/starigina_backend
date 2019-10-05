from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from .serializers import *
from .models import *

import json

class LoginAPIView(ObtainAuthToken):

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])
            user = serializer.validated_data['user']
            role = user.userprofile.role
            # if not created and token.created < timezone.now() - datetime.timedelta(hours=1):
            #     token.delete()
            #     token = Token.objects.create(user=serializer.validated_data['user'])
            #     token.created = timezone.now()
            #     token.save()
            json = {
                'id': user.id, 
                'token': token.key, 
                'username': user.username, 
                'email': user.email, 
                'first_name': user.first_name, 
                'last_name': user.last_name,
                'role': role
            }
            return Response(json, status=HTTP_200_OK)
        return Response({'error': 'Неверный логин или пароль'}, status=HTTP_400_BAD_REQUEST)



class LogoutAPIView(APIView):

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)



class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                role = Profile.objects.get(user=user).role
                json = serializer.data
                json['token'] = token.key
                json['role'] = role
                del json['password']
                return Response(json, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)