from apps.inventory.forms import StockItemForm


def test_stock_form_invalid_quantity(product):
    form = StockItemForm(data={"product": product.id, "quantity": -1, "low_stock_threshold": 1})
    assert not form.is_valid()
    assert "quantity" in form.errors
