# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.models import *
from core.serializers import *
from .models import *

@receiver(post_save, sender=StudentTest)
def new_test(sender, instance, created, **kwargs):
    if created:
        student_full_name = instance.student.userprofile.full_name
        student_username = instance.student.username
        test_name = instance.test.test_name
        if student_full_name is None:
            message = f'{student_username} прошел тест {test_name}'
        else:
            message = f'{student_full_name} прошел тест {test_name}'
        Notification.objects.create(to_user=instance.test.user, text=message)

@receiver(post_save, sender=Notification)
def new_norification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{instance.to_user.username}_room", {
                "type": "notificate",
                "event": "passed",
                "data": instance.text
            }
        )