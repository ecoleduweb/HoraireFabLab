from django.urls import path
from api.controllers.auth_controller import login,logout
from api.controllers.user_controller import me
from api.controllers.event_controller import create_event
from api.controllers.slot_controller import get_available_slots
from api.controllers.slot_controller import book_slot


urlpatterns = [
    path("login", login, name='login'),
    path("logout", logout, name="logout"),
    path("user/me", me, name='me'),
    path("events", create_event, name='create_event'),

    path("availableSlots/<int:event_id>", get_available_slots, name="get_available_slots"),
    path("book_slot", book_slot, name='book_slot'),
]
