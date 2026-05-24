from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.customers.forms import AddressForm, CustomerForm
from apps.customers.models import Address, Customer


@require_http_methods(["GET"])
def customer_list(request):
    data = list(Customer.objects.values("id", "name", "email", "phone"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def customer_create(request):
    form = CustomerForm(request.POST)
    if form.is_valid():
        customer = form.save()
        return JsonResponse({"id": customer.id, "name": customer.name}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


@require_http_methods(["POST"])
def address_create(request):
    form = AddressForm(request.POST)
    if form.is_valid():
        address = form.save()
        return JsonResponse({"id": address.id, "line1": address.line1}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
