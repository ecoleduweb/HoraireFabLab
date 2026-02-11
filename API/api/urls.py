from django.urls import path
from api.controllers.auth_controller import login

urlpatterns = [
    path("login/", login, name='login'),
]
