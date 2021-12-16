from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.test.client import Client
from django.urls.base import reverse

from .models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="test", email="test@test.com", password=make_password("test")
        )

    def test_login_page(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hobbies/login.html")

    def test_successful_login(self):
        response = self.client.post(
            reverse("user auth api"),
            {
                "email": "test@test.com",
                "password": "test",
            },
            content_type="application/json",
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hobbies/profile.html")

    def test_failed_login(self):
        response = self.client.post(
            reverse("user auth api"),
            {"email": "test@test.com", "password": "invalid password"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_authenticated_user(self):
        self.client.login(email="test@test.com", password="test")
        response = self.client.get(reverse("check auth"))

        self.assertRedirects(response, reverse("profile"), status_code=302)

    def test_non_authenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("check auth"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
