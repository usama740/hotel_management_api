"""
This module contains the API view for managing reservations.
It provides CRUD operations for creating, retrieving, updating, and deleting reservations.

Classes:
- ReservationView: Handles requests related to reservations (GET, POST, PUT, DELETE).
"""
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import Reservation
from ..repositories.reservation_repository import ReservationRepository
from ..serializers import ReservationSerializer
from ..utils.app_const import DefaultPaginationPageInfo

# Instantiate the ReservationRepository with the Reservation model
reservation_repo = ReservationRepository(Reservation)


class ReservationView(APIView):
    """
    API view for managing reservations.
    Handles CRUD operations for reservations: create, read, update, and delete.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ReservationSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Successfully created reservation",
                response=ReservationSerializer
            ),
        }
    )
    def post(self, request):
        """
        Handle POST requests to create a new reservation.

        Creates a new reservation for the authenticated user using the provided data.

        Returns:
            Response: A success or error response based on the creation outcome.
        """
        res, status_code = reservation_repo.create_reservation(
            user=request.user,
            data=request.data,
            reservation_serializer=ReservationSerializer
        )
        return Response(res, status=status_code)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                type=int,
                required=False,
                description='The page number for pagination (optional).'
            ),
            OpenApiParameter(
                name='page_size',
                type=int,
                required=False,
                description='The number of items per page (optional, defaults to 10).'
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiTypes.OBJECT,  # Returns list of reservations (paginated)
        }
    )
    def get(self, request):
        """
        Handle GET requests for reservations.

        If no reservation_id is provided, it fetches paginated reservations for the authenticated user.
        If a reservation_id is provided, it fetches the details of that specific reservation.

        Parameters:
            reservation_id (int): The ID of a specific reservation (optional).

        Returns:
            Response: A paginated list of reservations or a specific reservation.
        """
        # Set up pagination for the list of reservations
        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', DefaultPaginationPageInfo.PAGE_SIZE)
        paginator.page = request.query_params.get('page', DefaultPaginationPageInfo.PAGE_NO)

        # Fetch paginated reservations for the authenticated user
        reservations = reservation_repo.get_reservations_by_user(
            user=request.user,
            request=request,
            reservation_serializer=ReservationSerializer,
            paginator=paginator
        )
        return paginator.get_paginated_response(reservations)


class SingleReservationProcessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='reservation_id',
                type=int,
                required=True,
                description='The ID of the reservation to retrieve or update.'
            ),
            OpenApiParameter(
                name='page',
                type=int,
                required=False,
                description='The page number for pagination (optional).'
            ),
            OpenApiParameter(
                name='page_size',
                type=int,
                required=False,
                description='The number of items per page (optional, defaults to 10).'
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiTypes.OBJECT,
        }
    )
    def get(self, request, reservation_id):
        """
        Handle GET requests for a specific reservation by ID.

        Parameters:
            reservation_id (int): The ID of the reservation.

        Returns:
            Response: A specific reservation.
        """
        res, status_code = reservation_repo.get_reservation_by_id(
            reservation_id=reservation_id,
            user=request.user,
            reservation_serializer=ReservationSerializer,
        )
        return Response(res, status=status_code)

    @extend_schema(
        request=ReservationSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Successfully updated reservation",
                response=ReservationSerializer
            ),
        }
    )
    def put(self, request, reservation_id):
        """
        Handle PUT requests to update an existing reservation.

        Updates the reservation with the given reservation_id for the authenticated user.

        Parameters:
            reservation_id (int): The ID of the reservation to be updated.

        Returns:
            Response: A success or error response based on the update outcome.
        """
        res, status_code = reservation_repo.update_reservation(
            data=request.data,
            user=request.user,
            reservation_id=reservation_id,
            reservation_serializer=ReservationSerializer
        )
        return Response(res, status=status_code)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Successfully deleted reservation"
            ),
        }
    )
    def delete(self, request, reservation_id):
        """
        Handle DELETE requests to delete a reservation.

        Deletes the reservation with the given reservation_id for the authenticated user.

        Parameters:
            reservation_id (int): The ID of the reservation to be deleted.

        Returns:
            Response: A success or error response based on the deletion outcome.
        """
        res, status_code = reservation_repo.delete_reservation(
            reservation_id=reservation_id,
            user=request.user,
        )
        return Response(res, status=status_code)
