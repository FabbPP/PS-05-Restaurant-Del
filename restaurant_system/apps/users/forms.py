from __future__ import annotations

from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.core.validators import validate_phone
from apps.users.models import User


class UserRegisterForm(UserCreationForm):
    """Registration form with role and phone validation."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role", "phone")

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone", "")
        if phone:
            validate_phone(phone)
        return phone


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "role", "phone", "is_active")

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone", "")
        if phone:
            validate_phone(phone)
        return phone
