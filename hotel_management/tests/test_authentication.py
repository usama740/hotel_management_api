from rest_framework.test import APITestCase
from rest_framework import status

from hotel_management.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """
        Create a test user for authentication.
        """
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = "/api/auth/login"

    def test_user_can_login_and_receive_jwt(self):
        """
        Test that a user can log in and receive a JWT token.
        """
        # Make a POST request to the login endpoint with valid credentials
        response = self.client.post(self.login_url, {
            "username": self.username,
            "password": self.password
        })

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the access and refresh tokens
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_cannot_login_with_invalid_credentials(self):
        """
        Test that login fails with invalid credentials.
        """
        # Make a POST request to the login endpoint with invalid credentials
        response = self.client.post(self.login_url, {
            "username": self.username,
            "password": "wrongpassword"
        })

        # Assert that the response status is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert that the response does not contain tokens
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
