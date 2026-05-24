import pytest
from apps.dining.forms import TableForm

@pytest.mark.parametrize("number, capacity, is_valid", [
    (1, 1, True),         # AVL: Mínimo
    (200, 50, True),      # AVL: Máximo
    (100, 25, True),      # PE: Válido
    (0, 10, False),       # AVL: Fuera de límite inferior
    (1, 51, False),       # AVL: Fuera de límite superior
    ("NaN", 10, False),   # PE: Tipo inválido
    (1, float('nan'), False), # Robustez: NaN
    (1, float('inf'), False), # Robustez: Infinity
])
def test_table_form_robustness(number, capacity, is_valid):
    """Intento de romper el formulario de mesas con valores extremos."""
    form = TableForm(data={"number": number, "capacity": capacity, "status": "FREE"})
    assert form.is_valid() is is_valid

def test_table_form_malicious_input():
    """PE: Cadenas gigantes y espacios."""
    form = TableForm(data={"number": 1, "capacity": 5, "status": " " * 50})
    assert not form.is_valid()
    assert "status" in form.errors
