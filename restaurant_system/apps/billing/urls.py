from django.urls import path

from apps.billing import views

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("create/", views.invoice_create, name="invoice_create"),
]
