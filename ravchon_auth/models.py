from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

roles_choices = (
    (0,'Ученик'),
    (1,'Учитель')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.IntegerField(choices=roles_choices, default=0, verbose_name='Роль')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username
        
    @property
    def is_teacher(self):
        if self.role == 1:
            return True
        return False
        
    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.last_name} {self.user.first_name}"
        return None

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)