from django.db.models import Q

from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

from .models import *

import os
import json

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = ['pk', 'text']