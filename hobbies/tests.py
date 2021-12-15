from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.test.client import Client
from django.urls.base import reverse

from hobbies.models import User


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
