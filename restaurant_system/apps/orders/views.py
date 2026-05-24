from __future__ import annotations

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.orders.forms import OrderForm, OrderItemForm
from apps.orders.models import Order
from apps.core.exceptions import OrderStateError
from apps.core.exceptions import StockError
from apps.orders.services import add_item, change_status


@require_http_methods(["GET"])
def order_list(request):
    data = list(
        Order.objects.select_related("table", "customer").values(
            "id", "order_type", "status", "total", "table__number", "customer__name"
        )
    )
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def order_create(request):
    form = OrderForm(request.POST)
    if form.is_valid():
        order = form.save()
        return JsonResponse({"id": order.id, "status": order.status}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


@require_http_methods(["POST"])
def order_item_create(request):
    form = OrderItemForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        try:
            item = add_item(
                order=data["order"],
                product=data["product"],
                quantity=data["quantity"],
                unit_price=data["unit_price"],
            )
        except StockError as exc:
            return JsonResponse({"error": str(exc)}, status=400)
        return JsonResponse({"id": item.id, "subtotal": str(item.subtotal)}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


@require_http_methods(["POST"])
def order_change_status(request, order_id: int):
    new_status = request.POST.get("status")
    if not new_status:
        return JsonResponse({"error": "Estado requerido."}, status=400)
    order = get_object_or_404(Order, pk=order_id)
    try:
        change_status(order=order, new_status=new_status)
    except OrderStateError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    return JsonResponse({"id": order.id, "status": order.status})

# Create your views here.
