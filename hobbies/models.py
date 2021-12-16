from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Hobby(models.Model):
    name = models.TextField(max_length=200)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(max_length=200, unique=True)
    birthday = models.DateField(blank=True, null=True)
    city = models.TextField(blank=True, null=True, max_length=200)
    profile_image_url = models.URLField(blank=True, null=True, max_length=200)
    hobbies = models.ManyToManyField(Hobby)
    friends = models.ManyToManyField("self")

    def get_hobbies(self):
        return self.hobbies.all()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "birthday": self.birthday,
            "city": self.city,
            "profile_image_url": self.profile_image_url,
        }


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user"
    )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")

    def to_dict(self):
        return {
            "id": self.id,
            "from_user": self.from_user.to_dict(),
            "to_user": self.to_user.to_dict(),
        }
