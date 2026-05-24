from __future__ import annotations

from apps.core.enums import OrderStatus
from apps.core.exceptions import OrderStateError
from apps.orders.models import Order
from apps.payments.models import Payment


def confirm_payment(payment: Payment) -> Payment:
    if payment.order.status == OrderStatus.CANCELED:
        raise OrderStateError("No se puede pagar una orden cancelada.")
    payment.is_confirmed = True
    payment.save()

    order = payment.order
    order.status = OrderStatus.PAID
    order.save()
    return payment
