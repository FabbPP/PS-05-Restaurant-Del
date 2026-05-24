from __future__ import annotations

from django import forms

from apps.kitchen.models import KitchenTicket


class KitchenTicketForm(forms.ModelForm):
    class Meta:
        model = KitchenTicket
        fields = ("order", "status", "started_at", "completed_at")
