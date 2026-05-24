from apps.billing.services import create_invoice


def test_create_invoice(order_dine_in):
    order_dine_in.total = 10
    order_dine_in.save()
    invoice = create_invoice(
        order=order_dine_in,
        document_type="RECEIPT",
        document_number="B001-2",
        payment_method="CASH",
    )
    assert invoice.total_amount == order_dine_in.total
