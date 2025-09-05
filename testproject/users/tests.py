from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.password = "testpassword"
        self.user = User.objects.create(username="test")
        self.user.set_password(self.password)
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        url = reverse("users:register")
        data = {"username": "test_user", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = reverse("users:login")
        data = {"username": self.user.username, "password": self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        login_url = reverse("users:login")
        login_data = {"username": self.user.username, "password": self.password}
        login_response = self.client.post(login_url, login_data)
        refresh_token = login_response.data["refresh"]

        refresh_url = reverse("users:token_refresh")
        refresh_data = {"refresh": refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)
