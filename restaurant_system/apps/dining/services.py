from __future__ import annotations

import math
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import transaction, IntegrityError, DatabaseError
from django.core.exceptions import ValidationError

from apps.core.enums import TableStatus, OrderType, OrderStatus
from apps.core.utils import quantize_money
from apps.dining.models import Table

if TYPE_CHECKING:
    from apps.orders.models import Order, OrderItem
    from django.contrib.auth.models import User
    from apps.catalog.models import Product


class MesaOcupadaError(Exception):
    """Lanzada cuando se intenta abrir una mesa que no está en estado LIBRE."""
    pass


class StockInsuficienteError(Exception):
    """Lanzada cuando no hay existencias suficientes para añadir un producto."""
    pass


@transaction.atomic
def update_table_status(table: Table, status: str) -> Table:
    """Actualiza el estado de una mesa validando restricciones del modelo."""
    try:
        if not isinstance(table, Table):
            raise ValidationError("Instancia de mesa inválida.")
        table.status = status
        table.full_clean()
        table.save()
        return table
    except (IntegrityError, DatabaseError) as e:
        raise ValidationError(f"Error de base de datos al actualizar mesa: {e}")
    except Exception as e:
        raise ValidationError(f"Error inesperado al actualizar mesa: {e}")


@transaction.atomic
def create_table(*, number: int, capacity: int) -> Table:
    """Crea una mesa validando que los valores sean positivos y estén en rango."""
    try:
        if not all(isinstance(n, (int, float)) and math.isfinite(n) for n in [number, capacity]):
            raise ValidationError("Los valores numéricos deben ser finitos y válidos.")

        if number <= 0 or capacity <= 0:
            raise ValidationError("Número de mesa y capacidad deben ser mayores a cero.")
        
        table = Table(number=number, capacity=capacity)
        table.full_clean()
        table.save()
        return table
    except (IntegrityError, DatabaseError) as e:
        raise ValidationError(f"Error de integridad: ¿El número de mesa ya existe? ({e})")
    except Exception as e:
        raise ValidationError(f"Error inesperado al crear mesa: {e}")


@transaction.atomic
def open_table_session(*, table: Table, waiter: User) -> Order:
    """
    Inicia una sesión de comedor. 
    Cambia el estado de la mesa a OCUPADA y crea la Orden inicial.
    """
    try:
        if not isinstance(table, Table) or waiter is None:
            raise ValidationError("Mesa o mesero no válidos.")
        
        if not waiter.is_active:
            raise ValidationError("El mesero asignado no está activo en el sistema.")

        if table.status != TableStatus.FREE:
            raise MesaOcupadaError(f"La mesa {table.number} no está disponible (Estado: {table.status}).")

        from apps.orders.models import Order

        table.status = TableStatus.OCCUPIED
        table.save()

        return Order.objects.create(
            order_type=OrderType.DINE_IN,
            table=table,
            waiter=waiter,
            status=OrderStatus.PENDING
        )
    except MesaOcupadaError as e:
        raise ValidationError(str(e))
    except (IntegrityError, DatabaseError) as e:
        raise ValidationError(f"Error de persistencia al abrir sesión: {e}")


@transaction.atomic
def add_item_to_table_order(*, order: Order, product: Product, quantity: int) -> OrderItem:
    """
    Agrega un ítem a la orden de la mesa con control estricto de inventario.
    """
    try:
        from apps.inventory.models import StockItem
        from apps.inventory.services import adjust_stock
        from apps.orders.models import OrderItem
        from apps.orders.services import recalc_total

        if not isinstance(quantity, (int, float)) or not math.isfinite(quantity) or quantity <= 0:
            raise ValidationError("La cantidad debe ser un número finito mayor a cero.")

        # Bloqueo selectivo de fila para prevenir race conditions en stock
        stock = StockItem.objects.select_for_update().get(product=product)
        
        if stock.quantity < quantity:
            raise StockInsuficienteError(f"Stock insuficiente para '{product.name}'. Disponible: {stock.quantity}")

        # Protección de ajuste de stock
        try:
            adjust_stock(item=stock, delta=-quantity, reason="Consumo Comedor")
        except Exception as e:
            raise ValidationError(f"Fallo crítico al ajustar stock: {e}")

        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.price,
            subtotal=quantize_money(Decimal(quantity) * product.price)
        )
        recalc_total(order=order)
        return item
    except (StockItem.DoesNotExist, StockInsuficienteError) as e:
        raise ValidationError(str(e))
    except Exception as e:
        raise ValidationError(f"Error no controlado al agregar ítem: {e}")
