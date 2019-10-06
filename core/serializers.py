from django.db.models import Q

from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

from .models import *

import os
import json

class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)

class AnswerSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Answer
        fields = ('__all__')

class QuestionSerializer(DynamicFieldsModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('__all__')

    def create(self, validated_data):
        user = self.context['request'].user
        question = Question.objects.create(question_text=validated_data['question_text'], user=user)
        for a in validated_data['answers']:
            answer = Answer.objects.create(answer=a['answer'], score=a['score'], a=a['a'], b=a['b'], c=a['c'], pov=a['pov'], shel=a['shel'], user=user)
            question.answers.add(answer)
        return question

class TestListSerializer(DynamicFieldsModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, fields=["question_text"])

    class Meta:
        model = Test
        fields = ('__all__')

class TestDetailSerializer(DynamicFieldsModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ('__all__')

    def get_questions_count(self, obj):
        return len(obj.questions.all())

class StudentAnswerSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = StudentAnswer
        fields = ('__all__')

class StudentTestSerializer(DynamicFieldsModelSerializer):
    #test = TestDetailSerializer(fields=["id", "test_name"])
    questions = StudentAnswerSerializer(many=True)

    class Meta:
        model = StudentTest
        #fields = ('__all__')
        exclude = ['test']

    def create(self, validated_data):
        student = self.context['student']
        test = self.context['test']
        try:
            student_test = StudentTest.objects.get(Q(student=student) & Q(test=test) & Q(passed=False))
        except:
            student_test = StudentTest.objects.create(test=test, student=student)
        for q in validated_data['questions']:
            student_answer = StudentAnswer.objects.create(student=student, question=q['question'])
            for a in q['answers']:
                student_answer.answers.add(a)
            student_test.questions.add(student_answer)
        serializer = StudentTestSerializer(instance=student_test)
        return serializer.data

class StudentAnswerDetailSerializer(DynamicFieldsModelSerializer):
    question = QuestionSerializer(fields = ['id', 'question_text'])
    answers = AnswerSerializer(many=True, fields=["id", "answer", "a", "b", "c", "pov", "shel"])
    total = serializers.SerializerMethodField()

    class Meta:
        model = StudentAnswer
        fields = ('__all__')

    def get_total(self, obj):
       return obj.total_score

class StudentTestDetailSerializer(DynamicFieldsModelSerializer):
    test = TestDetailSerializer(fields=["id", "test_name"])
    questions = StudentAnswerDetailSerializer(many=True, exclude=['student'])
    student = serializers.SerializerMethodField()

    class Meta:
        model = StudentTest
        fields = ('__all__')

    def get_student(self, obj):
        return obj.student.username

class UserSerializer(DynamicFieldsModelSerializer):
    tests = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'tests']

    def get_tests(self, obj):
        instance = []
        username = self.context.get("request").parser_context['kwargs']['username']
        user = User.objects.get(username=username)
        tests = Test.objects.filter(user=user)
        for t in tests:
            instance.append(t)
        serializer = TestDetailSerializer(instance=instance, many=True, fields=['id', 'test_name', 'questions_count'])
        return serializer.data

class UserListSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']