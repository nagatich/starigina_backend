from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('tests/', ListView.as_view(model=Test, serializer_class=TestListSerializer)),
    path('tests/<int:pk>/', TestRUDView.as_view()),
    path('question/<int:pk>/', RUDView.as_view(model=Question, serializer_class=QuestionSerializer)),
    path('answer/<int:pk>/', RUDView.as_view(model=Answer, serializer_class=AnswerSerializer)),
    path('users/', UserListView.as_view()),
    path('users/<str:username>/', RView.as_view(model=User, serializer_class=UserSerializer)),
    path('students/<str:username>/tests/', StudentTestsView.as_view()),
    
    path('q/', Q.as_view())
]