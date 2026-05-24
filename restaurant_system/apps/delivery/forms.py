from __future__ import annotations

from decimal import Decimal
import re
import math
from django import forms

from apps.delivery.models import Courier, DeliveryInfo
from apps.delivery.services import calculate_fee, estimate_time


class CourierForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ("user", "is_available")


class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = (
            "order",
            "address",
            "phone",
            "distance_km",
            "delivery_fee",
            "estimated_time_min",
            "courier",
            "courier_status",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["delivery_fee"].required = False
        self.fields["estimated_time_min"].required = False

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        # Validación estricta: Solo dígitos, longitud 9 a 15 (formato internacional)
        if not re.match(r"^\d{9,15}$", phone):
            raise forms.ValidationError("El teléfono debe contener solo entre 9 y 15 dígitos numéricos.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get("address", "").strip()
        if not address:
            raise forms.ValidationError("La dirección de despacho es obligatoria.")
        if len(address) > 250:
            raise forms.ValidationError("La dirección es demasiado larga (máximo 250 caracteres).")
        return address

    def clean_distance_km(self):
        distance = self.cleaned_data.get("distance_km")
        if distance is None or not isinstance(distance, (Decimal, float, int)) or not math.isfinite(distance):
            raise forms.ValidationError("Valor de distancia inválido.")
        if distance <= 0:
            raise forms.ValidationError("La distancia debe ser mayor a cero.")
        if distance > Decimal("15.00"):
            raise forms.ValidationError("La distancia excede el límite de cobertura (15km).")
        return distance

    def clean(self):
        cleaned_data = super().clean()
        try:
            distance = cleaned_data.get("distance_km")
            if distance:
                # Cálculos automáticos seguros
                cleaned_data["delivery_fee"] = calculate_fee(distance)
                cleaned_data["estimated_time_min"] = estimate_time(distance)
            return cleaned_data
        except Exception as e:
            raise forms.ValidationError(f"Error en el cálculo de logística: {str(e)}")
