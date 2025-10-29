from django.db import models
from PIL import Image
from django.contrib.auth.models import User


# класс профиля пользователя связана с классом User связью Один-Ко-Одному
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # upload_to - указание директории для хранения фото аватарок пользователей
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    # изменение размера изображения(аватарки)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
