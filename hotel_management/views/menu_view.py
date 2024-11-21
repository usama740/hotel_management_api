"""
This module contains views for managing menu items.

Classes:
- MenuRetrieveListView: Handles the retrieval of a single menu item by ID or lists all menu items with pagination.
- MenuCreateView: Handles the creation, update, and deletion of menu items.
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import Menu
from ..repositories.menu_repository import MenuRepository
from ..serializers import MenuSerializer
from ..utils.app_const import DefaultPaginationPageInfo

# Instantiate the MenuRepository with the Menu model
menu_repo = MenuRepository(Menu)


class MenuRetrieveListView(APIView):
    """
    View to retrieve a single menu item by ID or list all menu items with user-provided pagination.
    """
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='menu_id',
                type=int,
                required=False,
                description='The ID of the menu item to retrieve (optional).'
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
            200: MenuSerializer(many=True),  # Response for paginated list of menu items
            200: MenuSerializer,  # Response for a single menu item
        }
    )
    def get(self, request, menu_id=None):
        """
        Handle GET requests to retrieve menu items.

        If menu_id is provided, fetch a specific menu item by its ID.
        If no menu_id is provided, return a paginated list of all menu items.

        Parameters:
            menu_id (int): The ID of the specific menu item (optional).

        Returns:
            Response: A single menu item or a paginated list of menu items.
        """
        if menu_id:
            # Retrieve a single menu item by ID
            res, status_code = menu_repo.get_single_menu_item(menu_item_id=menu_id, menu_serializer=MenuSerializer)
            return Response(res, status=status_code)
        else:
            # Set up pagination for the list of menu items
            paginator = PageNumberPagination()
            paginator.page_size = request.query_params.get('page_size', DefaultPaginationPageInfo.PAGE_SIZE)
            paginator.page = request.query_params.get('page', DefaultPaginationPageInfo.PAGE_NO)

            # Fetch paginated list of menu items
            res = menu_repo.get_menu_list(paginator=paginator, request=request, menu_serializer=MenuSerializer)
            return paginator.get_paginated_response(res)


class MenuCreateView(APIView):
    """
    View to create, update, or delete menu items.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=MenuSerializer,  # This tells Swagger what the expected request body will look like
        responses={status.HTTP_201_CREATED: MenuSerializer}  # This specifies the expected response format for a successful request
    )
    def post(self, request):
        """
        Handle POST requests to create a new menu item.

        Creates a new menu item with the provided data.

        Returns:
            Response: A success or error response based on the creation outcome.
        """
        res, status_code = menu_repo.create_menu_item(data=request.data, menu_serializer=MenuSerializer)
        return Response(res, status=status_code)


class MenuUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=MenuSerializer,
        responses={status.HTTP_200_OK: MenuSerializer}
    )
    def put(self, request, menu_id):
        """
        Handle PUT requests to update an existing menu item.

        Updates the menu item with the given menu_id using the provided data.

        Parameters:
            menu_id (int): The ID of the menu item to be updated.

        Returns:
            Response: A success or error response based on the update outcome.

        """
        res, status_code = menu_repo.update_menu_item(
            menu_item_id=menu_id,
            data=request.data,
            menu_serializer=MenuSerializer
        )
        return Response(res, status=status_code)

    @extend_schema(
        responses={status.HTTP_200_OK: 'Deleted successfully.'}
    )
    def delete(self, request, menu_id):
        """
        Handle DELETE requests to remove a menu item.

        Deletes the menu item with the given menu_id.

        Parameters:
            menu_id (int): The ID of the menu item to be deleted.

        Returns:
            Response: A success or error response based on the deletion outcome.
        """
        res, status_code = menu_repo.delete_menu_item(menu_item_id=menu_id)
        return Response(res, status=status_code)
