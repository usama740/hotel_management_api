"""
This module defines a `UserRepository` class responsible for handling user-related operations,
"""

from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import authenticate


class UserRepository:
    """
    Repository class for managing user-related actions.

    Attributes:
        model (model): The user model to be used for database interactions.
    """

    def __init__(self, user_model):
        """
        Initializes the UserRepository with a specific user model.

        Args:
            user_model (model): The user model to interact with the database.
        """
        self.model = user_model

    def create_user(self, data, user_serializer):
        """
        Creates a new user with the provided data and handles validation errors.

        Args:
            data (dict): Data to be validated and saved for the new user.
            user_serializer (serializer): The serializer used for user validation and saving.

        Raises:
            serializers.ValidationError: If validation fails, raises an error with custom messages.

        Returns:
            User: The created user object.
        """
        serializer = user_serializer(data=data)

        # Validate the data (using the custom validation logic in the serializer)
        if not serializer.is_valid():
            # Collect the errors manually from the serializer and return them
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    # Append the custom error messages
                    errors.append(f"{message}")

            # Raise a validation error with the custom error format
            raise serializers.ValidationError({"error": errors})

        # If validation is successful, save the user
        return serializer.save()

    def get_user_by_username(self, username):
        """
        Fetches a user by their username.

        Args:
            username (str): The username of the user to be fetched.

        Returns:
            User: The user object if found, otherwise None.
        """
        return self.model.objects.filter(username=username).first()

    def login_user(self, username, password, request, custom_refresh_token):
        """
        Authenticates a user with the provided username and password.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password for the user attempting to log in.
            request (HttpRequest): The HTTP request object, used for authentication.
            custom_refresh_token (object): A custom token object used to generate refresh tokens.

        Returns:
            tuple: A tuple containing a response dictionary and the status code.
        """
        if not username or not password:
            res = {"error": "Username and password are required"}
            res_status = status.HTTP_400_BAD_REQUEST

        else:
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is None:
                res = {"error": "Invalid credentials"}
                res_status = status.HTTP_401_UNAUTHORIZED

            else:
                # Generate the custom refresh and access tokens
                refresh = custom_refresh_token.for_user(user)  # Use the customized token
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Return the tokens and the user_id in the response
                res = {
                    "access": access_token,
                    "refresh": refresh_token
                }
                res_status = status.HTTP_200_OK

        return res, res_status
