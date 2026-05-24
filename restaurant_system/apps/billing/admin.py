from django.contrib import admin

from apps.billing.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("document_type", "document_number", "total_amount", "is_paid")

# Register your models here.
