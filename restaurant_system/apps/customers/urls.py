from django.urls import path

from apps.customers import views

urlpatterns = [
    path("", views.customer_list, name="customer_list"),
    path("create/", views.customer_create, name="customer_create"),
    path("addresses/create/", views.address_create, name="address_create"),
]
