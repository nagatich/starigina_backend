from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.db.models import Q

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED
)

import json

from .models import *
from .serializers import *
from .permissions import *

class ListView(mixins.CreateModelMixin, generics.ListAPIView):
    model = None
    #permission_classes = [IsTeacher]

    def get_queryset(self):
        if self.model is not None:
            return self.model.objects.all()
        else:
            return None

    def perform_create(self):
        self.serializer_class.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RView(generics.RetrieveAPIView):
    lookup_field = 'username'
    model = None

    def get_queryset(self):
        if self.model is not None:
            return self.model.objects.all()
        else:
            return None

class RUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    permission_classes = [IsOwnerOrReadOnly]
    model = None

    def get_queryset(self):
        if self.model is not None:
            return self.model.objects.all()
        else:
            return None

class QuestionListView(mixins.CreateModelMixin, generics.ListAPIView):
    model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TestRUDView(generics.RetrieveUpdateDestroyAPIView):
    model = Test
    serializer_class = TestDetailSerializer

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        role = request.user.userprofile.role
        try:
            test = self.model.objects.get(pk=kwargs['pk'])
        except:
            return Response(status=HTTP_404_NOT_FOUND)
        if role == 1:
            question = QuestionSerializer(data=request.data, context = {'request': request})
            if question.is_valid():
                question = question.save()
                test.questions.add(question)
                return Response(status=HTTP_201_CREATED)
            return Response(status=HTTP_400_BAD_REQUEST)
        if role == 0:
            student = request.user
            context = {
                'student': student,
                'test': test
            }
            student_test = None
            for data in request.data:
                serializer = StudentTestSerializer(data=data, context=context)
                if serializer.is_valid():
                    student_test = serializer.save()
                else:
                    student_test = serializer.errors
            return Response(student_test)
        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        test = self.model.objects.get(pk=kwargs['pk'])
        if request.user != test.user:
            return Response(status=HTTP_403_FORBIDDEN)
        else:
            return super(TestRUDView, self).delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        test = self.model.objects.get(pk=kwargs['pk'])
        if request.user != test.user:
            return Response(status=HTTP_403_FORBIDDEN)
        else:
            return super(TestRUDView, self).update(request, *args, **kwargs)

class UserListView(generics.ListAPIView):
    model = User
    serializer_class = UserListSerializer

    def get_queryset(self):
        qs = self.model.objects.all()
        for key, value in self.request.GET.items():
            if key == 'students':
                qs = self.model.objects.filter(userprofile__role=0)
            if key == 'teachers':
                qs = self.model.objects.filter(userprofile__role=1)
        return qs

class StudentTestsView(generics.ListAPIView):
    model = StudentTest
    serializer_class = StudentTestDetailSerializer

    def get_queryset(self):
        user = User.objects.get(username=self.request.parser_context['kwargs']['username'])
        qs = self.model.objects.filter(student=user)
        return qs

class Q(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        return Response({'kek': 1})