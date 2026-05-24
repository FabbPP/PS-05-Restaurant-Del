from apps.core.enums import OrderStatus
from apps.payments.models import Payment
from apps.payments.services import confirm_payment


def test_confirm_payment_updates_order(order_dine_in):
    order_dine_in.total = 10
    order_dine_in.save()
    payment = Payment.objects.create(order=order_dine_in, method="CASH", amount=10)
    confirm_payment(payment)
    order_dine_in.refresh_from_db()
    assert order_dine_in.status == OrderStatus.PAID
