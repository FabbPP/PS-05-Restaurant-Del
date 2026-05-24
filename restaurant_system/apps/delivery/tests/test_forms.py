import pytest
from decimal import Decimal
from apps.delivery.forms import DeliveryInfoForm


@pytest.mark.parametrize("phone, is_valid", [
    ("999888777", True),        # PE: Clase Válida (9 dígitos)
    ("123456789012345", True),  # AVL: Límite superior (15 dígitos según regex)
    ("888777", False),          # AVL: Bajo el límite inferior
    ("abcdefghi", False),       # PE: Clase Inválida (Letras)
    ("999 888 777", False),     # PE: Clase Inválida (Espacios)
    ("", False),                # PE: Clase Nula
])
def test_delivery_form_phone_validation(order_delivery, phone, is_valid):
    """Prueba el blindaje del campo teléfono mediante PE y AVL."""
    data = {
        "order": order_delivery.id,
        "address": "Calle Principal 123",
        "phone": phone,
        "distance_km": 5.0,
    }
    form = DeliveryInfoForm(data=data)
    assert form.is_valid() is is_valid
    if not is_valid:
        assert "phone" in form.errors


@pytest.mark.parametrize("address, is_valid", [
    ("Av. Siempreviva 742", True),  # Clase Válida
    ("   ", False),                 # Clase Inválida: Solo espacios
    ("A" * 251, False),             # AVL: Excede límite de 250 caracteres
    ("", False),                    # Clase Nula
])
def test_delivery_form_address_robustness(order_delivery, address, is_valid):
    """Evalúa la resistencia del campo dirección ante entradas maliciosas o vacías."""
    data = {
        "order": order_delivery.id,
        "address": address,
        "phone": "999888777",
        "distance_km": 1.0,
    }
    form = DeliveryInfoForm(data=data)
    assert form.is_valid() is is_valid


@pytest.mark.parametrize("distance, is_valid", [
    (0.1, True),                # AVL: Justo sobre cero
    (15.0, True),               # AVL: Límite de cobertura
    (15.1, False),              # AVL: Fuera de cobertura
    (-5.0, False),              # PE: Clase Inválida (Negativo)
    (float('nan'), False),      # Robustez: NaN
])
def test_delivery_form_distance_math(order_delivery, distance, is_valid):
    """Verifica que los cálculos matemáticos de tarifas no acepten valores basura."""
    data = {
        "order": order_delivery.id,
        "address": "Calle Falsa 123",
        "phone": "999888777",
        "distance_km": distance,
    }
    form = DeliveryInfoForm(data=data)
    assert form.is_valid() is is_valid
