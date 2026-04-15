from django.urls import path
from api.controllers.auth_controller import login,logout
from api.controllers.user_controller import me
from api.controllers.event_controller import update_event_date


urlpatterns = [
    path("login", login, name='login'),
    path("logout", logout, name="logout"),
    path("user/me", me, name='me'),
    path("events/<int:event_id>/update_date/", update_event_date, name="update_event_date"),

]
