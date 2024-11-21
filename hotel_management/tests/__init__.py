"""
This module imports the test cases for the authentication, menu, and reservation functionalities.
These test classes ensure that the application's core features, such as user authentication, 
menu item CRUD operations, and reservation CRUD operations, are working correctly.

Test Cases:
- AuthenticationTests: Contains tests for user authentication and login functionality.
- MenuCRUDTests: Contains tests for creating, reading, updating, and deleting menu items.
- ReservationCRUDTests: Contains tests for creating, reading, updating, and deleting reservations.
"""

# Importing the test classes
from .test_authentication import AuthenticationTests
from .test_menu import MenuCRUDTests
from .test_reservations import ReservationCRUDTests
