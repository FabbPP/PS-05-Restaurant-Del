import pytest
from django.core.exceptions import ValidationError
from apps.dining.services import (
    update_table_status, create_table, open_table_session, add_item_to_table_order
)
from apps.core.enums import TableStatus


@pytest.mark.parametrize("number, capacity, should_pass", [
    (10, 4, True),    # PE: Clase Válida
    (1, 1, True),     # AVL: Límite inferior válido
    (0, 4, False),    # AVL: Fuera de límite (0)
    (-1, 4, False),   # PE: Clase Inválida (Negativo)
    (5, -2, False),   # PE: Clase Inválida (Capacidad negativa)
    (float('nan'), 4, False), # Robustez: NaN
])
def test_create_table_pe_avl(number, capacity, should_pass):
    """Evalúa la creación de mesas con Partición de Equivalencia y Valores Límite."""
    if should_pass:
        table = create_table(number=number, capacity=capacity)
        assert table.number == number
    else:
        with pytest.raises(ValidationError):
            create_table(number=number, capacity=capacity)


def test_open_table_session_errors(table, waiter):
    """Pruebas de PE para apertura de sesión de mesa."""
    # 1. PE: Clase Nula/Vacía (Sin mesero)
    with pytest.raises(ValidationError, match="Mesa o mesero no válidos"):
        open_table_session(table=table, waiter=None)

    # 2. PE: Mesero inactivo
    waiter.is_active = False
    waiter.save()
    with pytest.raises(ValidationError, match="no está activo"):
        open_table_session(table=table, waiter=waiter)
    
    # 3. AVL: Mesa ya ocupada (Lanza MesaOcupadaError capturado como ValidationError)
    waiter.is_active = True
    waiter.save()
    open_table_session(table=table, waiter=waiter)
    with pytest.raises(ValidationError, match="no está disponible"):
        open_table_session(table=table, waiter=waiter)


@pytest.mark.parametrize("quantity, should_pass, error_msg", [
    (5, True, None),               # PE: Clase Válida (Stock inicial 10)
    (10, True, None),              # AVL: Límite exacto de stock
    (11, False, "insuficiente"),   # AVL: Fuera de límite (+1)
    (0, False, "mayor a cero"),    # PE/AVL: Límite inválido
    (-1, False, "mayor a cero"),   # PE: Clase Inválida
    (float('inf'), False, "finito"),# Robustez: Infinity
])
def test_add_item_stock_control(order_dine_in, product, stock_item, quantity, should_pass, error_msg):
    """Validación de control de stock usando PE y AVL."""
    if should_pass:
        item = add_item_to_table_order(order=order_dine_in, product=product, quantity=quantity)
        assert item.quantity == quantity
        stock_item.refresh_from_db()
        assert stock_item.quantity == 10 - quantity
    else:
        with pytest.raises(ValidationError) as exc:
            add_item_to_table_order(order=order_dine_in, product=product, quantity=quantity)
        if error_msg:
            assert error_msg in str(exc.value).lower()


def test_update_table_status_robustness(table):
    """Verifica que el sistema no se caiga ante instancias inválidas en servicios."""
    # PE: Clase Inválida (No es instancia de Table)
    with pytest.raises(ValidationError, match="Instancia de mesa inválida"):
        update_table_status(table="not-a-table", status=TableStatus.OCCUPIED)

    # Transición válida
    update_table_status(table, TableStatus.CLEANING)
    table.refresh_from_db()
    assert table.status == TableStatus.CLEANING
