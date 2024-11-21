"""
Module for managing custom refresh tokens with specific expiration times.
"""
import os
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    """
    A custom implementation of RefreshToken with configurable expiration times.
    """

    def for_user(self, user):
        """
        Generates a refresh token for the given user with custom expiration times.

        - Refresh token expiration time is set using the 'REFRESH_TOKEN_LIFETIME'
          environment variable (default: 1440 minutes).
        - Access token expiration time is set using the 'ACCESS_TOKEN_LIFETIME'
          environment variable (default: 5 minutes).

        Args:
            user: The user instance for whom the token is generated.

        Returns:
            RefreshToken: A customized refresh token instance.
        """
        refresh = super().for_user(user)

        # Set refresh token expiry (from .env file or default value)
        refresh.set_exp(lifetime=timedelta(minutes=int(os.getenv("REFRESH_TOKEN_LIFETIME", 1440))))

        # Set custom access token expiry
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_LIFETIME", 5))))

        return refresh
