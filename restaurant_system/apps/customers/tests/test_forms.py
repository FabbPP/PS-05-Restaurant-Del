from apps.customers.forms import CustomerForm


def test_customer_form_invalid_phone():
    form = CustomerForm(data={"name": "Test", "email": "test@example.com", "phone": "abc"})
    assert not form.is_valid()
    assert "phone" in form.errors
