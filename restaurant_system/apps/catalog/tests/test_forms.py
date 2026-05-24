from apps.catalog.forms import ProductForm


def test_product_form_invalid_price(category):
    form = ProductForm(data={"category": category.id, "name": "Test", "price": "0.00"})
    assert not form.is_valid()
    assert "price" in form.errors
