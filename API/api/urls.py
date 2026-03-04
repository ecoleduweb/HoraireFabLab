from django.urls import path
from api.controllers.auth_controller import login,logout
from api.controllers.user_controller import me


urlpatterns = [
    path("login/", login, name='login'),
    path("logout/", logout, name="logout"),
    path("user/me/", me, name='me'),

]
