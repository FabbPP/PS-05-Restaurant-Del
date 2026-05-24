from apps.payments.forms import PaymentForm


def test_payment_form_invalid_amount(order_dine_in):
    form = PaymentForm(data={"order": order_dine_in.id, "method": "CASH", "amount": 0})
    assert not form.is_valid()
    assert "amount" in form.errors
