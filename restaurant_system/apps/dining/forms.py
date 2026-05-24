from __future__ import annotations

from django import forms

from apps.core.validators import validate_int_range
from apps.dining.models import Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ("number", "capacity", "status")

    def clean_number(self):
        number = self.cleaned_data.get("number")
        validate_int_range(number, 1, 200)
        return number

    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity")
        validate_int_range(capacity, 1, 50)
        return capacity
