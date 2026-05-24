import pytest
from django.core.exceptions import ValidationError
from apps.dining.models import Table

@pytest.mark.parametrize("number, capacity", [
    (1, 0),    # AVL: Mínimo inválido
    (201, 10), # AVL: Máximo excedido
    (-1, 5),   # PE: Negativo
])
def test_table_constraints_pe_avl(number, capacity):
    """Valida restricciones de integridad del modelo Table."""
    table = Table(number=number, capacity=capacity)
    with pytest.raises(ValidationError):
        table.full_clean()

def test_table_unique_number(db):
    """PE: Evitar duplicados de llaves naturales."""
    Table.objects.create(number=10, capacity=4)
    with pytest.raises(Exception): # IntegrityError
        Table.objects.create(number=10, capacity=2)
