"""
This module defines the `Menu` model, which represents a menu item in a restaurant.
"""

from django.db import models


class Menu(models.Model):
    """
    Represents a menu item in a restaurant.
    Attributes:
        name (str): The name of the menu item (e.g., 'Pizza').
        description (str): A detailed description of the menu item.
        price (Decimal): The price of the menu item.
        created_at (datetime): The timestamp when the menu item was created.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the menu item, typically its name.

        Returns:
            str: The name of the menu item.
        """
        return self.name
