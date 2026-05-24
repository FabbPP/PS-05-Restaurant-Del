from django.urls import path

from apps.payments import views

urlpatterns = [
    path("", views.payment_list, name="payment_list"),
    path("create/", views.payment_create, name="payment_create"),
    path("<int:payment_id>/confirm/", views.payment_confirm, name="payment_confirm"),
]
