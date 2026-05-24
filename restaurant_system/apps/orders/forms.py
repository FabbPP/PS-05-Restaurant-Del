from __future__ import annotations

from decimal import Decimal
import math

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
        """Blindaje de caja negra contra strings vacíos, largos o nulos."""
        cleaned_data = super().clean()
        try:
            order_type = cleaned_data.get("order_type")
            table = cleaned_data.get("table")
            customer = cleaned_data.get("customer")

            # Validación lógica de negocio
            if order_type == OrderType.DINE_IN and not table:
                self.add_error("table", "Mesa requerida para órdenes en mesa.")
            if order_type == OrderType.DELIVERY:
                if not customer:
                    self.add_error("customer", "Cliente requerido para delivery.")
                if table:
                    self.add_error("table", "Una orden de delivery no puede tener mesa asignada.")

            # Control de entradas maliciosas en campos de texto (si los hubiera en el futuro)
            for field, value in cleaned_data.items():
                if isinstance(value, str):
                    if not value.strip():
                        self.add_error(field, "Este campo no puede contener solo espacios en blanco.")
                    if len(value) > 255:
                        self.add_error(field, "Entrada excesivamente larga detectada.")
            return cleaned_data
        except Exception as e:
            raise forms.ValidationError(f"Fallo crítico en validación: {str(e)}")


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ("order", "product", "quantity")

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity is None or not isinstance(quantity, (int, float)) or not math.isfinite(quantity):
            raise forms.ValidationError("Cantidad inválida.")
        validate_int_range(quantity, 1, 100)
        return quantity

    def save(self, commit: bool = True) -> OrderItem:
        instance = super().save(commit=False)
        instance.unit_price = instance.product.price
        instance.subtotal = quantize_money(Decimal(instance.quantity) * instance.unit_price)
        if commit:
            instance.save()
        return instance
