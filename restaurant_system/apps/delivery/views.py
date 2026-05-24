from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.delivery.forms import CourierForm, DeliveryInfoForm
from apps.delivery.models import DeliveryInfo
from apps.delivery.services import update_delivery_cost


@require_http_methods(["GET"])
def delivery_list(request):
    data = list(
        DeliveryInfo.objects.select_related("order").values(
            "id", "order_id", "distance_km", "delivery_fee", "estimated_time_min", "courier_status"
        )
    )
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def delivery_create(request):
    form = DeliveryInfoForm(request.POST)
    if form.is_valid():
        delivery = form.save()
        update_delivery_cost(delivery)
        return JsonResponse({"id": delivery.id, "fee": str(delivery.delivery_fee)}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


@require_http_methods(["POST"])
def courier_create(request):
    form = CourierForm(request.POST)
    if form.is_valid():
        courier = form.save()
        return JsonResponse({"id": courier.id}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
