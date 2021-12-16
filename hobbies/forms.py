from django.forms import ModelForm

from .models import User


class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "city", "birthday", "profile_image_url"]
