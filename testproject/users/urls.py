from django.urls import path

from .apps import UsersConfig
from .views import UserCreateAPIView


app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),

]
