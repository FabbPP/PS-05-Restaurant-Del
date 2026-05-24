from __future__ import annotations

from django import forms

from apps.billing.models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("order", "document_type", "document_number", "total_amount", "payment_method", "is_paid")
