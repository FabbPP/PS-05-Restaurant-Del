from __future__ import annotations

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(*, username: str, password: str, role: str, email: str = "", phone: str = ""):
    user = User.objects.create_user(username=username, password=password, role=role, email=email, phone=phone)
    return user
