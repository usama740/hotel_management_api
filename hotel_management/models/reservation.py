"""
This module defines the `Reservation` model, which represents a room reservation booked by a user.
"""

from django.db import models
from .user import User


class Reservation(models.Model):
    """
    Represents a room reservation in a booking system.
    Attributes:
        user (ForeignKey): A reference to the user who made the reservation.
        room_number (str): The room number reserved by the user.
        check_in_date (date): The date when the user is expected to check in.
        check_out_date (date): The date when the user is expected to check out.
        created_at (datetime): The timestamp when the reservation was created.
        updated_at (datetime): The timestamp when the reservation was last updated.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the reservation.

        Returns:
            str: A formatted string representing the reservation.
        """
        return f"Reservation {self.id} by {self.user.username} from {self.check_in_date} to {self.check_out_date}"
