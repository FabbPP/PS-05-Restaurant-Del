from __future__ import annotations

from apps.catalog.models import Product


def set_product_active(product: Product, is_active: bool) -> Product:
    product.is_active = is_active
    product.save()
    return product
