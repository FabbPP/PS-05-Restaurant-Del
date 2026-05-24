from __future__ import annotations

from django import forms

from apps.core.validators import validate_phone
from apps.customers.models import Address, Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "email", "phone", "user")

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone", "")
        validate_phone(phone)
        return phone


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("customer", "line1", "line2", "city", "reference", "is_default")
