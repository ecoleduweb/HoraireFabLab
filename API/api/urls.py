from django.urls import path
from api.controllers.auth_controller import login
from api.controllers.user_controller import me


urlpatterns = [
    path("login/", login, name='login'),
    path("user/me/", me, name='me'),

]
