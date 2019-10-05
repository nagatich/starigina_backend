from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    text = models.CharField(max_length=512, verbose_name='Текст уведомления')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Для пользователя')
    seen = models.BooleanField(default=False, verbose_name='Прочитано')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        
    def __str__(self):
        return self.to_user.username