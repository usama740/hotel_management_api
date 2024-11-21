"""
This module defines the `MenuRepository` class responsible for handling menu-related
operations.
"""

from rest_framework import status, serializers


class MenuRepository:
    """
    Repository class for managing menu item-related actions.

    Attributes:
        model (model): The menu model used for database interactions.
    """

    def __init__(self, menu_model):
        """
        Initializes the MenuRepository with a specific menu model.

        Args:
            menu_model (model): The menu model to interact with the database.
        """
        self.model = menu_model

    def create_menu_item(self, data, menu_serializer):
        """
        Creates a new menu item with the provided data.

        Args:
            data (dict): The menu item data to be validated and saved.
            menu_serializer (serializer): The serializer used for validating and saving the menu item.

        Returns:
            tuple: A tuple containing the serialized menu item data and HTTP status code.

        Raises:
            serializers.ValidationError: If the data is not valid according to the serializer.
        """
        serializer = menu_serializer(data=data)

        # Validate the data (using the custom validation logic in the serializer)
        if serializer.is_valid():
            menu_item = self.model.objects.create(**data)
            res = menu_serializer(menu_item).data
            status_code = status.HTTP_201_CREATED
            return res, status_code
        else:
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    # Append the custom error messages
                    errors.append(f"{message}")

            # Raise a validation error with the custom error format
            raise serializers.ValidationError({"error": errors})

    def get_menu_list(self, paginator, request, menu_serializer):
        """
        Retrieves a list of all menu items, paginated.

        Args:
            paginator (Paginator): The paginator used to handle pagination of the results.
            request (HttpRequest): The request object, used for pagination.
            menu_serializer (serializer): The serializer used to format the menu items.

        Returns:
            list: A list of serialized menu item data.
        """
        menu_items = self.model.objects.all()
        paginated_menu_items = paginator.paginate_queryset(menu_items, request)
        serializer = menu_serializer(paginated_menu_items, many=True)
        return serializer.data

    def get_menu_item_by_id(self, menu_id):
        """
        Retrieves a specific menu item by its ID.

        Args:
            menu_id (int): The ID of the menu item to be retrieved.

        Returns:
            object: The menu item if found, or None if not.
        """
        return self.model.objects.filter(id=menu_id).first()

    def update_menu_item(self, menu_item_id, data, menu_serializer):
        """
        Updates an existing menu item with new data.

        Args:
            menu_item_id (int): The ID of the menu item to be updated.
            data (dict): The data to update the menu item with.
            menu_serializer (serializer): The serializer used for validating and updating the menu item.

        Returns:
            tuple: A tuple containing the response data (updated menu item or errors) and HTTP status code.
        """
        menu_item = self.get_menu_item_by_id(menu_item_id)
        if menu_item is None:
            return {"error": "Menu not found."}, status.HTTP_404_NOT_FOUND
        serializer = menu_serializer(menu_item, data=data, partial=True)

        # Validate the data (using the custom validation logic in the serializer)
        if serializer.is_valid():
            serializer.save()
            return serializer.data, status.HTTP_200_OK
        return serializer.errors, status.HTTP_400_BAD_REQUEST

    def delete_menu_item(self, menu_item_id):
        """
        Deletes a menu item by its ID.

        Args:
            menu_item_id (int): The ID of the menu item to be deleted.

        Returns:
            tuple: A tuple containing a success message and HTTP status code.
        """
        menu_item = self.get_menu_item_by_id(menu_item_id)
        if menu_item is None:
            return {"error": "Menu not found."}, status.HTTP_404_NOT_FOUND
        menu_item.delete()
        return {"message": "Menu deleted successfully"}, status.HTTP_200_OK

    def get_single_menu_item(self, menu_item_id, menu_serializer):
        """
        Retrieves a specific menu item by its ID, serialized.

        Args:
            menu_item_id (int): The ID of the menu item to be retrieved.
            menu_serializer (serializer): The serializer used to format the menu item data.

        Returns:
            tuple: A tuple containing the serialized menu item data and HTTP status code.
        """
        menu_item = self.get_menu_item_by_id(menu_item_id)
        if menu_item is None:
            return {"error": "Menu not found."}, status.HTTP_404_NOT_FOUND
        return menu_serializer(menu_item).data, status.HTTP_200_OK
