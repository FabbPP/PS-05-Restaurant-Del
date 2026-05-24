from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.dining.forms import TableForm
from apps.dining.models import Table


@require_http_methods(["GET"])
def table_list(request):
    data = list(Table.objects.values("id", "number", "capacity", "status"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def table_create(request):
    form = TableForm(request.POST)
    if form.is_valid():
        table = form.save()
        return JsonResponse({"id": table.id, "number": table.number}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
