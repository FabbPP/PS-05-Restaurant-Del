import pytest
from django.core.exceptions import ValidationError

from django.utils import timezone

from apps.kitchen.models import KitchenTicket


def test_kitchen_ticket_invalid_dates(order_dine_in):
    ticket = KitchenTicket(order=order_dine_in, completed_at=timezone.now())
    with pytest.raises(ValidationError):
        ticket.full_clean()
