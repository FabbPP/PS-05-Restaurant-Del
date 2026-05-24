from django.urls import path

from apps.inventory import views

urlpatterns = [
    path("stock/", views.stock_list, name="stock_list"),
    path("stock/create/", views.stock_create, name="stock_create"),
    path("stock/movements/create/", views.stock_movement_create, name="stock_movement_create"),
]
