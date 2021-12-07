from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.


class Hobby(models.Model):
    name = models.TextField(max_length=200)


class User(AbstractUser):
    username = models.TextField(max_length=200, unique=True)
    password = models.TextField(max_length=200)
    img = models.URLField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    city = models.TextField(max_length=200)
    birthday = models.DateTimeField(default=timezone.now)
    hobbies = models.ManyToManyField(Hobby)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.img,
            'username': self.username,
            'email': self.email,
            'date': self.birthday,
            'city': self.city,
            'api': reverse('user api', kwargs={'user_id': self.id}),
        }
