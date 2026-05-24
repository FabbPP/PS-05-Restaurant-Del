from django.urls import path

from apps.dining import views

urlpatterns = [
    path("tables/", views.table_list, name="table_list"),
    path("tables/create/", views.table_create, name="table_create"),
]
