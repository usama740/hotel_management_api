from rest_framework.test import APITestCase
from rest_framework import status

from hotel_management.models import Menu, User


class MenuCRUDTests(APITestCase):
    def setUp(self):
        """
        Set up test users and initial data.
        """
        # Create a user
        self.user = User.objects.create_user(username="testuser1", password="password123")

        # Get token
        token_url = "/api/auth/login"
        token_response = self.client.post(
            token_url,
            {"username": "testuser1", "password": "password123"},
            format="json"
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK, token_response.data)

        # Store the token and set it in the Authorization header
        self.token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Define API endpoints
        self.menu_url = "/api/menu"
        self.menu_get_url = "/api/menu/get"

        # Create a menu item for testing
        self.menu_item = Menu.objects.create(
            name="menu1",
            description="Test menu description",
            price=15.0
        )

    def test_create_menu_authenticated(self):
        """
        Test creating a menu item as an authenticated user.
        """
        payload = {
            "name": "menu2",
            "description": "A test menu item",
            "price": 12
        }
        response = self.client.post(self.menu_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payload["name"])
        self.assertEqual(response.data["description"], payload["description"])
        self.assertEqual(response.data["price"], payload["price"])

    def test_create_menu_unauthenticated(self):
        """
        Test that unauthenticated users cannot create a menu item.
        """
        self.client.logout()
        payload = {
            "name": "menu2",
            "description": "A test menu item",
            "price": 12.0
        }
        response = self.client.post(self.menu_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_menu_authenticated(self):
        """
        Test updating a menu item as an authenticated user.
        """
        payload = {
            "name": "Updated menu",
            "description": "Updated description",
            "price": 20.0
        }
        url = f"{self.menu_url}/{self.menu_item.id}"
        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], payload["name"])
        self.assertEqual(response.data["description"], payload["description"])
        self.assertEqual(response.data["price"], payload["price"])

    def test_update_menu_unauthenticated(self):
        """
        Test that unauthenticated users cannot update a menu item.
        """
        self.client.logout()
        payload = {
            "name": "Updated menu",
            "description": "Updated description",
            "price": 20.0
        }
        url = f"{self.menu_url}/{self.menu_item.id}"
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_menu_authenticated(self):
        """
        Test deleting a menu item as an authenticated user.
        """
        url = f"{self.menu_url}/{self.menu_item.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Menu.objects.filter(id=self.menu_item.id).exists())

    def test_delete_menu_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete a menu item.
        """
        self.client.logout()
        url = f"{self.menu_url}/{self.menu_item.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_menu_list(self):
        """
        Test fetching the menu list for any user (authenticated or unauthenticated).
        """
        self.client.logout()  # Test unauthenticated access
        response = self.client.get(self.menu_get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_menu_single(self):
        """
        Test fetching a single menu item for any user (authenticated or unauthenticated).
        """
        self.client.logout()  # Test unauthenticated access
        url = f"{self.menu_get_url}/{self.menu_item.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.menu_item.name)
        self.assertEqual(response.data["description"], self.menu_item.description)
        self.assertEqual(response.data["price"], self.menu_item.price)
