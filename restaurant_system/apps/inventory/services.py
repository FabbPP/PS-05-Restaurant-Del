from __future__ import annotations

from django.db import transaction

from apps.core.exceptions import StockError
from apps.inventory.models import StockItem, StockMovement


@transaction.atomic
def adjust_stock(*, item: StockItem, delta: int, reason: str) -> StockItem:
    new_quantity = item.quantity + delta
    if new_quantity < 0:
        raise StockError("El stock no puede ser negativo.")
    item.quantity = new_quantity
    item.save()
    StockMovement.objects.create(item=item, delta=delta, reason=reason)
    return item
