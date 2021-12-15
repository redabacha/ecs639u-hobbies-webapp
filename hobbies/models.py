from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.


class Hobby(models.Model):
    name = models.TextField(max_length=200)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(max_length=200, unique=True)
    img = models.URLField(max_length=200)
    city = models.TextField(max_length=200)
    birthday = models.DateTimeField(default=timezone.now)
    hobbies = models.ManyToManyField(Hobby)

    def getHobbies(self):
        hobbies = []
        for h1 in Hobby.objects.all():
            for h2 in self.hobbies.all():
                if h1 == h2:
                    hobbies.append(h1)
        return hobbies

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.img,
            "username": self.username,
            "email": self.email,
            "date": self.birthday,
            "city": self.city,
            "api": reverse("user api", kwargs={"user_id": self.id}),
        }
