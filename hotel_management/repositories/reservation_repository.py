"""
This module defines the `ReservationRepository` class responsible for handling reservation-related
operations.
"""

from rest_framework import status


class ReservationRepository:
    """
    Repository class for managing reservation-related actions.

    Attributes:
        model (model): The reservation model used for database interactions.
    """

    def __init__(self, reservation_model):
        """
        Initializes the ReservationRepository with a specific reservation model.

        Args:
            reservation_model (model): The reservation model to interact with the database.
        """
        self.model = reservation_model

    def create_reservation(self, user, data, reservation_serializer):
        """
        Creates a new reservation for a user with the provided data.

        Args:
            user (User): The user creating the reservation.
            data (dict): The reservation data to be validated and saved.
            reservation_serializer (serializer): The serializer used for reservation validation and saving.

        Returns:
            tuple: A tuple containing the response data and HTTP status code.
        """
        serializer = reservation_serializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            new_reservation = self.model.objects.create(user=user, **validated_data)
            new_reservation.save()
            res = reservation_serializer(new_reservation).data
            status_code = status.HTTP_201_CREATED
        else:
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    # Append the custom error messages
                    errors.append(f"{message}")
            res = {"errors": errors}
            status_code = status.HTTP_400_BAD_REQUEST

        return res, status_code

    def get_reservations_by_user(self, user, paginator, request, reservation_serializer):
        """
        Retrieves all reservations for a specified user.

        Args:
            user (User): The user whose reservations are being retrieved.
            paginator (Paginator): The paginator used to handle pagination of the results.
            request (HttpRequest): The request object, used for pagination.
            reservation_serializer (serializer): The serializer used to format the reservations.

        Returns:
            list: A list of serialized reservation data for the user.
        """
        reservations = self.model.objects.filter(user=user).all()
        paginated_reservations = paginator.paginate_queryset(reservations, request)
        serializer = reservation_serializer(paginated_reservations, many=True)
        return serializer.data

    def get_reservation_by_id(self, reservation_id, user, reservation_serializer):
        """
        Retrieves a specific reservation by its ID for a specified user.

        Args:
            reservation_id (int): The ID of the reservation to be fetched.
            user (User): The user requesting the reservation.
            reservation_serializer (serializer): The serializer used to format the reservation data.

        Returns:
            tuple: A tuple containing the response data and HTTP status code.
        """
        reservation = self.model.objects.filter(id=reservation_id, user=user).first()
        if reservation:
            res = reservation_serializer(reservation).data
            status_code = status.HTTP_200_OK
        else:
            res = {"errors": f"Reservation with ID {reservation_id} not found."}
            status_code = status.HTTP_404_NOT_FOUND

        return res, status_code

    def update_reservation(self, reservation_id, data, user, reservation_serializer):
        """
        Updates an existing reservation with new data.

        Args:
            reservation_id (int): The ID of the reservation to be updated.
            data (dict): The data to update the reservation with.
            user (User): The user making the update request.
            reservation_serializer (serializer): The serializer used for validating and updating the reservation.

        Returns:
            tuple: A tuple containing the response data and HTTP status code.
        """
        reservation = self.model.objects.filter(id=reservation_id, user=user).first()
        if not reservation:
            res = {"error": f"Reservation with id {reservation_id} not found."}
            status_code = status.HTTP_404_NOT_FOUND
        else:
            serializer = reservation_serializer(reservation, data=data, partial=True)
            if serializer.is_valid():
                for key, value in data.items():
                    setattr(reservation, key, value)
                reservation.save()
                res = reservation_serializer(reservation).data
                status_code = status.HTTP_200_OK
            else:
                errors = []
                for field, messages in serializer.errors.items():
                    for message in messages:
                        # Append the custom error messages
                        errors.append(f"{message}")
                res = {"errors": errors}
                status_code = status.HTTP_400_BAD_REQUEST

        return res, status_code

    def delete_reservation(self, reservation_id, user):
        """
        Deletes a reservation by its ID for the specified user.

        Args:
            reservation_id (int): The ID of the reservation to be deleted.
            user (User): The user requesting the deletion of the reservation.

        Returns:
            tuple: A tuple containing the response data and HTTP status code.
        """
        reservation = self.model.objects.filter(id=reservation_id, user=user).first()
        if reservation:
            reservation.delete()
            res = {"message": f"Reservation deleted successfully."}
            status_code = status.HTTP_200_OK
        else:
            res = {"error": f"Reservation with id {reservation_id} not found."}
            status_code = status.HTTP_404_NOT_FOUND
        return res, status_code
