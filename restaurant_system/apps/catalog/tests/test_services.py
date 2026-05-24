from apps.catalog.services import set_product_active


def test_set_product_active(db, product):
    set_product_active(product, False)
    product.refresh_from_db()
    assert product.is_active is False
