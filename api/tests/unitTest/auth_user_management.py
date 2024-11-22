from django.test import TestCase
from django.urls import reverse
from api.models import *

class AuthUserManagement(TestCase):
    # Registration Test
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "password",
            "password2": "password",
            "account_type": "buyer"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    # Log in Test
    def test_user_login(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="password",
            account_type="buyer"
        )

        response = self.client.post(reverse('login'),{
            "username": "testuser",
            "password": "password",
            "account_type": "buyer"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    # Log out Test
    def test_user_logout(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="password",
            account_type="buyer"
        )

        self.client.login(username="testuser", password="password")

        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    # Delete account test
    def test_delete_account(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="password",
            account_type="buyer"
        )

        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="testuser").exists())
