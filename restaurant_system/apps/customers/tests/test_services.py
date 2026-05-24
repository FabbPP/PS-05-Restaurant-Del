from apps.customers.models import Address
from apps.customers.services import set_default_address


def test_set_default_address(db, customer):
    address = Address.objects.create(customer=customer, line1="Av 1", city="Lima")
    set_default_address(customer, address)
    address.refresh_from_db()
    assert address.is_default is True
