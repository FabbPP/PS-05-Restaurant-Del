from django.urls import path

from apps.orders import views

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.order_create, name="order_create"),
    path("items/create/", views.order_item_create, name="order_item_create"),
    path("<int:order_id>/status/", views.order_change_status, name="order_change_status"),
]
