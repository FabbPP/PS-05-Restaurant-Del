from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.inventory.forms import StockItemForm, StockMovementForm
from apps.inventory.models import StockItem


@require_http_methods(["GET"])
def stock_list(request):
    data = list(StockItem.objects.select_related("product").values("id", "product__name", "quantity"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def stock_create(request):
    form = StockItemForm(request.POST)
    if form.is_valid():
        item = form.save()
        return JsonResponse({"id": item.id, "product": item.product.name}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


@require_http_methods(["POST"])
def stock_movement_create(request):
    form = StockMovementForm(request.POST)
    if form.is_valid():
        movement = form.save()
        return JsonResponse({"id": movement.id, "delta": movement.delta}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
