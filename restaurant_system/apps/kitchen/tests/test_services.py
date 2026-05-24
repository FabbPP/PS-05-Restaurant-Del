from apps.kitchen.models import KitchenTicket
from apps.kitchen.services import start_ticket


def test_start_ticket(order_dine_in):
    ticket = KitchenTicket.objects.create(order=order_dine_in)
    start_ticket(ticket)
    ticket.refresh_from_db()
    assert ticket.started_at is not None
