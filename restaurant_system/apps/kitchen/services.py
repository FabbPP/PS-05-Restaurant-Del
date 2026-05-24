from __future__ import annotations

from django.utils import timezone

from apps.kitchen.models import KitchenTicket


def start_ticket(ticket: KitchenTicket) -> KitchenTicket:
    ticket.started_at = timezone.now()
    ticket.save()
    return ticket
