from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Perfil", {"fields": ("role", "phone")}),
    )
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")

# Register your models here.
