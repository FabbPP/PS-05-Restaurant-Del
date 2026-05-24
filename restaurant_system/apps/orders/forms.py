from __future__ import annotations

from decimal import Decimal

from django import forms

from apps.core.enums import OrderType
from apps.core.utils import quantize_money
from apps.core.validators import validate_int_range
from apps.orders.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("order_type", "table", "customer", "waiter")

    def clean(self):
        cleaned = super().clean()
        order_type = cleaned.get("order_type")
        table = cleaned.get("table")
        customer = cleaned.get("customer")
        if order_type == OrderType.DINE_IN and not table:
            self.add_error("table", "Mesa requerida para órdenes en mesa.")
        if order_type == OrderType.DELIVERY and not customer:
            self.add_error("customer", "Cliente requerido para delivery.")
        if order_type == OrderType.DELIVERY and table:
            self.add_error("table", "Delivery no debe tener mesa.")
        return cleaned


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ("order", "product", "quantity")

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        validate_int_range(quantity, 1, 100)
        return quantity

    def save(self, commit: bool = True) -> OrderItem:
        instance = super().save(commit=False)
        instance.unit_price = instance.product.price
        instance.subtotal = quantize_money(Decimal(instance.quantity) * instance.unit_price)
        if commit:
            instance.save()
        return instance
