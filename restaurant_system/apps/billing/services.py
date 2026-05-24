from __future__ import annotations

from apps.billing.models import Invoice
from apps.orders.models import Order


def create_invoice(*, order: Order, document_type: str, document_number: str, payment_method: str) -> Invoice:
    invoice = Invoice(
        order=order,
        document_type=document_type,
        document_number=document_number,
        total_amount=order.total,
        payment_method=payment_method,
        is_paid=False,
    )
    invoice.save()
    return invoice
