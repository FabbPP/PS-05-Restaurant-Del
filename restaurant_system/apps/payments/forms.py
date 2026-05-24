from __future__ import annotations

from django import forms

from apps.core.validators import validate_positive_decimal
from apps.payments.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("order", "method", "amount", "is_confirmed")

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        validate_positive_decimal(amount)
        return amount

    def clean(self):
        cleaned = super().clean()
        order = cleaned.get("order")
        amount = cleaned.get("amount")
        if order and amount is not None and amount < order.total:
            self.add_error("amount", "El monto no cubre el total.")
        return cleaned
