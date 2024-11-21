"""
This module contains API views related to user authentication and registration.

Classes:
- UserRegistrationView: Handles user registration requests.
- UserLoginView: Handles user login requests.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..repositories.user_repository import UserRepository
from ..serializers import UserSerializer
from ..utils.auth_utils import CustomRefreshToken

# Instantiate the UserRepository with the User model
user_repo = UserRepository(User)

class UserRegistrationView(APIView):
    """
    API view for user registration.
    Handles the POST request to create a new user.
    """

    def post(self, request):
        """
        Handle POST request for user registration.

        Returns:
            Response: A response indicating the success or failure of the user creation.
        """
        try:
            # Create user using the repository and the provided serializer
            user = user_repo.create_user(data=request.data, user_serializer=UserSerializer)
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            # Handle any errors (e.g., validation errors) during user creation
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    API view for user login.
    Handles the POST request to authenticate a user and generate tokens.
    """

    def post(self, request):
        """
        Handle POST request for user login.

        Returns:
            Response: A response containing authentication results, including tokens.
        """
        # Extract username and password from request data
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        # Attempt to log in the user using the repository
        res, status_code = user_repo.login_user(
            username=username,
            password=password,
            request=request,
            custom_refresh_token=CustomRefreshToken()
        )

        # Return the response with the appropriate status code
        return Response(res, status=status_code)
