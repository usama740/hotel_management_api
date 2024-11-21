from rest_framework.test import APITestCase
from rest_framework import status

from hotel_management.models import Reservation, User


class ReservationCRUDTests(APITestCase):
    def setUp(self):
        """
        Set up test users and initial data.
        """
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.reservation_url = "/api/reservations"

        # Get token for user1
        token_url = "/api/auth/login"
        token_response = self.client.post(
            token_url,
            {"username": "user1", "password": "password123"},
            format="json"
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK, token_response.data)

        # Store the token and set it in the Authorization header
        self.token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Create a reservation for user1
        self.reservation = Reservation.objects.create(
            user=self.user1,
            room_number=1,
            check_in_date="2024-01-01",
            check_out_date="2024-01-02"
        )

    def test_create_reservation(self):
        """
        Test creating a reservation.
        """
        payload = {
            "room_number": 2,
            "check_in_date": "2024-01-04",
            "check_out_date": "2024-01-05"
        }
        response = self.client.post(self.reservation_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["room_number"], payload["room_number"])
        self.assertEqual(response.data["check_in_date"], payload["check_in_date"])
        self.assertEqual(response.data["check_out_date"], payload["check_out_date"])

    def test_update_reservation(self):
        """
        Test updating a reservation.
        """
        payload = {
            "room_number": 1,
            "check_in_date": "2024-01-03",
            "check_out_date": "2024-01-04"
        }
        url = f"{self.reservation_url}/{self.reservation.id}"
        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["room_number"], payload["room_number"])
        self.assertEqual(response.data["check_in_date"], payload["check_in_date"])
        self.assertEqual(response.data["check_out_date"], payload["check_out_date"])

    def test_get_reservation_list(self):
        """
        Test fetching the reservation list for the logged-in user.
        """
        response = self.client.get(self.reservation_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Only user1's reservation is returned

    def test_get_single_reservation(self):
        """
        Test fetching a single reservation.
        """
        url = f"{self.reservation_url}/{self.reservation.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["room_number"], self.reservation.room_number)

    def test_delete_reservation(self):
        """
        Test deleting a reservation.
        """
        url = f"{self.reservation_url}/{self.reservation.id}"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_reservation_access_restriction(self):
        """
        Test that a reservation belonging to another user is not accessible.
        """
        token_url = "/api/auth/login"
        token_response = self.client.post(
            token_url,
            {"username": "user2", "password": "password123"},
            format="json"
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK, token_response.data)

        # Store the token and set it in the Authorization header
        self.token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        url = f"{self.reservation_url}/{self.reservation.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

