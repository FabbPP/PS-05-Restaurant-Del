import pytest
from apps.core.enums import OrderType
from apps.orders.forms import OrderForm


def test_order_form_invalid_delivery_without_customer():
    form = OrderForm(data={"order_type": OrderType.DELIVERY})
    assert not form.is_valid()
    assert "customer" in form.errors

@pytest.mark.robustness
@pytest.mark.parametrize("malicious_input", [
    "A" * 500,              # Giant string
    "{\"json\": \"hack\"}", # Caracteres especiales
    "   ",                  # Whitespace
    "NULL",                 # PE: Falsos nulos
    "<script>alert(1)</script>", # XSS attempt
])
def test_order_form_blackbox_robustness(malicious_input):
    """PE/Robustez: Intento de romper el OrderForm con inputs peligrosos."""
    form = OrderForm(data={
        "order_type": OrderType.DINE_IN,
        "table": 1,
        "customer": malicious_input # Si el campo aceptara string
    })
    # El formulario debe invalidar strings gigantes o vacíos según clean() implementado
    assert not form.is_valid()
