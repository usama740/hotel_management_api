# urls.py

from django.urls import path
from hotel_management.views import (
    UserRegistrationView,
    MenuRetrieveListView,
    MenuCreateView,
    MenuUpdateView,
    UserLoginView,
    SingleReservationProcessView,
    ReservationView

)
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView


urlpatterns = [
    # User endpoints
    path('user', UserRegistrationView.as_view(), name='user-list-create'),
    path('auth/login', UserLoginView.as_view(), name='user-login'),

    # Reservation endpoints
    path('reservations', ReservationView.as_view(), name='reservation'),
    path('reservations/<int:reservation_id>', SingleReservationProcessView.as_view(), name='reservation-detail'),

    # Menu endpoints
    path('menu', MenuCreateView.as_view(), name='menu-create'),
    path('menu/<int:menu_id>', MenuUpdateView.as_view(), name='menu-update'),
    path('menu/get/<int:menu_id>', MenuRetrieveListView.as_view(), name='menu-detail'),  # GET by ID
    path('menu/get', MenuRetrieveListView.as_view(), name='menu-list'),  # GET list with pagination

    # Api Docs
    path('schema', SpectacularAPIView.as_view(), name='schema-json'),

    # Swagger UI
    path('docs/swagger', SpectacularSwaggerView.as_view(url_name='schema-json'), name='swagger-ui'),

]
