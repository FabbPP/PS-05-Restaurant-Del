from __future__ import annotations

from django import forms

from apps.catalog.models import Category, Product
from apps.core.validators import validate_decimal_range


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "name", "description", "price", "is_active")

    def clean_price(self):
        price = self.cleaned_data.get("price")
        validate_decimal_range(price, 0.01, 9999.99)
        return price
