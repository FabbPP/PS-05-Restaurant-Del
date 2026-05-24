from __future__ import annotations

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.payments.forms import PaymentForm
from apps.payments.models import Payment
from apps.payments.services import confirm_payment


@require_http_methods(["GET"])
def payment_list(request):
    data = list(Payment.objects.values("id", "order_id", "amount", "method", "is_confirmed"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def payment_create(request):
    form = PaymentForm(request.POST)
    if form.is_valid():
        payment = form.save()
        return JsonResponse({"id": payment.id}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


@require_http_methods(["POST"])
def payment_confirm(request, payment_id: int):
    payment = get_object_or_404(Payment, pk=payment_id)
    confirm_payment(payment)
    return JsonResponse({"id": payment.id, "is_confirmed": payment.is_confirmed})

# Create your views here.
