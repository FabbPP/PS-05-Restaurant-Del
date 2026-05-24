from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.kitchen.forms import KitchenTicketForm
from apps.kitchen.models import KitchenTicket


@require_http_methods(["GET"])
def ticket_list(request):
    data = list(KitchenTicket.objects.values("id", "order_id", "status"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def ticket_create(request):
    form = KitchenTicketForm(request.POST)
    if form.is_valid():
        ticket = form.save()
        return JsonResponse({"id": ticket.id, "status": ticket.status}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
