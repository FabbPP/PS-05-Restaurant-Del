from apps.billing.forms import InvoiceForm


def test_invoice_form_missing_number(order_dine_in):
    form = InvoiceForm(
        data={
            "order": order_dine_in.id,
            "document_type": "RECEIPT",
            "total_amount": 10,
            "payment_method": "CASH",
            "is_paid": False,
        }
    )
    assert not form.is_valid()
    assert "document_number" in form.errors
