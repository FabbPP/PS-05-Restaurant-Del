from django.urls import path

from apps.delivery import views

urlpatterns = [
    path("", views.delivery_list, name="delivery_list"),
    path("create/", views.delivery_create, name="delivery_create"),
    path("couriers/create/", views.courier_create, name="courier_create"),
]
