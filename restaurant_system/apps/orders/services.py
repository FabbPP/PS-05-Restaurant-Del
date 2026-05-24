from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from apps.core.enums import OrderStatus, OrderType, TableStatus
from apps.core.exceptions import OrderStateError, StockError
from apps.core.utils import quantize_money
from apps.inventory.models import StockItem
from apps.inventory.services import adjust_stock
from apps.orders.models import Order, OrderItem, OrderStatusHistory


@transaction.atomic
def create_order(*, order_type: str, table=None, customer=None, waiter=None) -> Order:
    if order_type == OrderType.DINE_IN and table:
        if table.status != TableStatus.FREE:
            raise OrderStateError("La mesa no está disponible.")
        table.status = TableStatus.OCCUPIED
        table.save()
    order = Order(order_type=order_type, table=table, customer=customer, waiter=waiter)
    order.save()
    return order


@transaction.atomic
def add_item(*, order: Order, product, quantity: int, unit_price: Decimal) -> OrderItem:
    if order.status not in {OrderStatus.PENDING, OrderStatus.PREPARING}:
        raise OrderStateError("La orden no permite agregar items en este estado.")

    try:
        stock = StockItem.objects.select_for_update().get(product=product)
    except StockItem.DoesNotExist as exc:
        raise StockError("Producto sin stock configurado.") from exc
    if not product.is_active:
        raise StockError("Producto inactivo.")

    if stock.quantity < quantity:
        raise StockError("Stock insuficiente.")

    adjust_stock(item=stock, delta=-quantity, reason="order_item")

    item = OrderItem(order=order, product=product, quantity=quantity, unit_price=unit_price, subtotal=Decimal("0.00"))
    item.save()

    recalc_total(order=order)
    return item


def recalc_total(*, order: Order) -> None:
    total = sum((item.subtotal for item in order.items.all()), Decimal("0.00"))
    order.total = quantize_money(total)
    order.save()


@transaction.atomic
def change_status(*, order: Order, new_status: str) -> None:
    allowed = {
        OrderStatus.PENDING: {OrderStatus.PREPARING, OrderStatus.CANCELED},
        OrderStatus.PREPARING: {OrderStatus.READY, OrderStatus.CANCELED},
        OrderStatus.READY: {OrderStatus.DELIVERED},
        OrderStatus.DELIVERED: {OrderStatus.PAID},
        OrderStatus.PAID: set(),
        OrderStatus.CANCELED: set(),
    }
    if new_status == order.status or new_status not in allowed.get(order.status, set()):
        raise OrderStateError("Transición de estado inválida.")
    OrderStatusHistory.objects.create(order=order, from_status=order.status, to_status=new_status)
    order.status = new_status
    order.save()
    if order.table and new_status in {OrderStatus.PAID, OrderStatus.CANCELED}:
        order.table.status = TableStatus.CLEANING if new_status == OrderStatus.PAID else TableStatus.FREE
        order.table.save()


def can_close_order(order: Order) -> bool:
    if order.order_type == OrderType.DELIVERY and not hasattr(order, "delivery_info"):
        return False
    return order.total >= 0
