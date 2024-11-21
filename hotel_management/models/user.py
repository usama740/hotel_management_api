"""
This module defines the `User` model, which extends Django's built-in `AbstractUser` model.
It adds an optional phone number field to store additional contact information for the user.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Represents a user in the application, extending Django's default `AbstractUser`.
    Attributes:
        phone_number (str): An optional field to store the user's phone number.
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the username.

        Returns:
            str: The username of the user.
        """
        return self.username
