from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', RegisterAPIView.as_view())
]