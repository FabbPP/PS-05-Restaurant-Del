from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.billing.forms import InvoiceForm
from apps.billing.models import Invoice


@require_http_methods(["GET"])
def invoice_list(request):
    data = list(Invoice.objects.values("id", "document_type", "document_number", "total_amount", "is_paid"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def invoice_create(request):
    form = InvoiceForm(request.POST)
    if form.is_valid():
        invoice = form.save()
        return JsonResponse({"id": invoice.id, "number": invoice.document_number}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
