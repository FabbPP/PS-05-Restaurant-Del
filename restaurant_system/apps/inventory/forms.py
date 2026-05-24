from __future__ import annotations

from django import forms

from apps.core.validators import validate_int_range
from apps.inventory.models import StockItem, StockMovement


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ("product", "quantity", "low_stock_threshold")

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        validate_int_range(quantity, 0, 99999)
        return quantity

    def clean_low_stock_threshold(self):
        threshold = self.cleaned_data.get("low_stock_threshold")
        validate_int_range(threshold, 1, 9999)
        return threshold


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ("item", "delta", "reason")
