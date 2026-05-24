from __future__ import annotations

import math
from django import forms

from apps.core.validators import validate_int_range
from apps.core.enums import TableStatus
from apps.dining.models import Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ("number", "capacity", "status")

    def clean_number(self):
        number = self.cleaned_data.get("number")
        if number is None or not isinstance(number, (int, float)) or not math.isfinite(number):
            raise forms.ValidationError("Número de mesa inválido o no proporcionado.")
        validate_int_range(number, 1, 200)
        return number

    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity")
        if capacity is None or not isinstance(capacity, (int, float)) or not math.isfinite(capacity):
            raise forms.ValidationError("Capacidad inválida o no proporcionada.")
        validate_int_range(capacity, 1, 50)
        return capacity

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if not status:
            return TableStatus.FREE
        if status not in TableStatus.values:
            raise forms.ValidationError("El estado seleccionado no es válido.")
        return status

    def clean(self):
        """
        Blindaje general (Enfoque Caja Negra) contra entradas maliciosas
        o lógicamente inconsistentes.
        """
        cleaned_data = super().clean()
        try:
            for field, value in cleaned_data.items():
                # Validar cadenas: vacías, solo espacios o excesivamente largas
                if isinstance(value, str):
                    stripped_value = value.strip()
                    if not stripped_value:
                        self.add_error(field, "Este campo no puede estar vacío o contener solo espacios.")
                    if len(value) > 100:
                        self.add_error(field, "Longitud de entrada fuera de los límites de seguridad (máx 100).")
            return cleaned_data
        except Exception as e:
            raise forms.ValidationError(f"Error crítico en validación de formulario: {str(e)}")
