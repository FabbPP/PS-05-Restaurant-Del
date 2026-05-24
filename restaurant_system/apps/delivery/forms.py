from __future__ import annotations

from decimal import Decimal

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

    def clean_distance_km(self):
        distance = self.cleaned_data.get("distance_km")
        if distance is None or distance < 0 or distance > Decimal("15.00"):
            raise forms.ValidationError("Fuera de cobertura.")
        return distance

    def clean(self):
        cleaned = super().clean()
        distance = cleaned.get("distance_km")
        if distance is not None:
            cleaned["delivery_fee"] = calculate_fee(distance)
            cleaned["estimated_time_min"] = estimate_time(distance)
        return cleaned
