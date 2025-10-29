from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

"""
В общем, вышеприведенный код делает то, что после того, как метод 
модели пользователя save() завершил выполнение, он отправляет сигнал 
post_save в функцию-приемник create_profile, затем эта функция 
получит сигнал для создания и сохранения экземпляра профиля для 
этого пользователя.
"""
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)