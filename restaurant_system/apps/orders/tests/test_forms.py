from apps.core.enums import OrderType
from apps.orders.forms import OrderForm


def test_order_form_invalid_delivery_without_customer():
    form = OrderForm(data={"order_type": OrderType.DELIVERY})
    assert not form.is_valid()
    assert "customer" in form.errors
