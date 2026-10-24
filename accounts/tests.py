
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.signup_url = "/api/signup/"
        self.login_url = "/api/login/"
        self.profile_url = "/api/profile/"
        self.refresh_url = "/api/token/refresh/"
        self.verify_url = "/api/token/verify/"

        self.password = "Safe-Test-Password-482!"

        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password=self.password,
        )

    def test_signup_creates_user_and_hashes_password(self):
        password = "Safe-Bob-Password-582!"

        response = self.client.post(
            self.signup_url,
            {
                "username": "bob",
                "email": "bob@example.com",
                "password": password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bob = User.objects.get(username="bob")

        self.assertNotEqual(bob.password, password)
        self.assertTrue(bob.check_password(password))
        self.assertNotIn("password", response.data)

    def test_signup_rejects_duplicate_email(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "bob",
                "email": "alice@example.com",
                "password": "Safe-Bob-Password-582!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_signup_rejects_weak_password(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "bob",
                "email": "bob@example.com",
                "password": "123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(User.objects.filter(username="bob").exists())

    def test_login_returns_access_and_refresh_tokens(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "alice",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_rejects_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "alice",
                "password": "Wrong-Password-123!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_profile_requires_authentication(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_profile_accepts_valid_access_token(self):
        # Obtain a real access token through the login endpoint.
        login_response = self.client.post(
            self.login_url,
            {
                "username": "alice",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access_token = login_response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "alice")
        self.assertEqual(response.data["email"], "alice@example.com")

    def test_profile_rejects_invalid_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer invalid-token"
        )

        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_returns_new_access_token(self):
        login_response = self.client.post(
            self.login_url,
            {
                "username": "alice",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        refresh_response = self.client.post(
            self.refresh_url,
            {"refresh": login_response.data["refresh"]},
            format="json",
        )

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("access", refresh_response.data)

    def test_token_verify_accepts_valid_access_token(self):
        login_response = self.client.post(
            self.login_url,
            {
                "username": "alice",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        token = login_response.data["access"]

        response = self.client.post(
            self.verify_url,
            {"token": token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_verify_rejects_invalid_token(self):
        response = self.client.post(
            self.verify_url,
            {"token": "invalid-token"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
