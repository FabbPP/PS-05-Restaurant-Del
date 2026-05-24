from __future__ import annotations

from apps.customers.models import Address, Customer


def set_default_address(customer: Customer, address: Address) -> None:
    customer.addresses.update(is_default=False)
    address.is_default = True
    address.save()
