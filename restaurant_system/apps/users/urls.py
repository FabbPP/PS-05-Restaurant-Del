from django.urls import path
from django.contrib.auth import views as auth_views

from apps.users import views

app_name = "users"

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path("create/", views.user_create, name="user_create"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
]
