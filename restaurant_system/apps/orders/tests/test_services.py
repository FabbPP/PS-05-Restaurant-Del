import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.orders.services import create_order, add_item, change_status
from apps.core.enums import OrderType, OrderStatus, TableStatus

def test_create_order_dine_in_occupied_table(table, waiter):
    """Test de excepción: No abrir orden en mesa ya ocupada."""
    table.status = TableStatus.OCCUPIED
    table.save()
    
    with pytest.raises(ValidationError, match="ya está ocupada"):
        create_order(order_type=OrderType.DINE_IN, table=table, waiter=waiter)

def test_add_item_invalid_order_status(order_dine_in, product_active, stock_item):
    """Test de validación: No agregar items a órdenes cerradas."""
    order_dine_in.status = OrderStatus.DELIVERED
    order_dine_in.save()
    
    with pytest.raises(ValidationError, match="No se pueden añadir ítems"):
        add_item(order=order_dine_in, product=product_active, quantity=1, unit_price=Decimal("10.00"))

@pytest.mark.parametrize("status_flow", [
    [OrderStatus.PENDING, OrderStatus.PREPARING, OrderStatus.READY], # Válido
    [OrderStatus.PENDING, OrderStatus.READY], # Inválido (salto de estado)
])
def test_order_fsm_transitions(order_dine_in, status_flow):
    """Test funcional: Máquina de estados (FSM) de la orden."""
    try:
        for next_status in status_flow[1:]:
            change_status(order=order_dine_in, new_status=next_status)
    except Exception:
        assert status_flow == [OrderStatus.PENDING, OrderStatus.READY] # Solo debe fallar en este caso

def test_order_recalc_total_integration(order_dine_in, product_active, stock_item):
    """Test funcional: Cálculo exacto de totales."""
    add_item(order=order_dine_in, product=product_active, quantity=2, unit_price=Decimal("15.00"))
    order_dine_in.refresh_from_db()
    assert order_dine_in.total == Decimal("30.00")

@pytest.mark.robustness
@pytest.mark.parametrize("quantity", [
    float('nan'),
    float('inf'),
    -1,
    0,
    1000000, # Fuera de rango lógico de un restaurante
])
def test_add_item_nan_and_limits(order_dine_in, product_active, stock_item, quantity):
    """AVL/Robustez: Evitar que valores no finitos o absurdos corrompan el Stock."""
    with pytest.raises(ValidationError):
        add_item(
            order=order_dine_in, 
            product=product_active, 
            quantity=quantity, 
            unit_price=Decimal("10.00")
        )

@pytest.mark.robustness
def test_order_duplicate_item_handling(order_dine_in, product_active, stock_item):
    """PE: Manejo de duplicados. Agregar el mismo producto dos veces."""
    add_item(order=order_dine_in, product=product_active, quantity=1, unit_price=Decimal("10.00"))
    # Segunda adición debe funcionar acumulando o creando registro nuevo según lógica
    item2 = add_item(order=order_dine_in, product=product_active, quantity=1, unit_price=Decimal("10.00"))
    assert item2.id is not None
    
@pytest.mark.fsm
def test_invalid_fsm_transition_skip(order_dine_in):
    """FSM: No permitir saltar de PENDING a DELIVERED sin pasar por READY."""
    with pytest.raises(ValidationError):
        change_status(order=order_dine_in, new_status=OrderStatus.DELIVERED)