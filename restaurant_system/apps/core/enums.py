from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Administrador"
    WAITER = "WAITER", "Mesero"
    COOK = "COOK", "Cocinero"
    COURIER = "COURIER", "Repartidor"
    CUSTOMER = "CUSTOMER", "Cliente"


class TableStatus(models.TextChoices):
    FREE = "FREE", "Libre"
    OCCUPIED = "OCCUPIED", "Ocupada"
    RESERVED = "RESERVED", "Reservada"
    CLEANING = "CLEANING", "Limpiando"


class OrderType(models.TextChoices):
    DINE_IN = "DINE_IN", "Mesa"
    DELIVERY = "DELIVERY", "Delivery"


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pendiente"
    PREPARING = "PREPARING", "Preparando"
    READY = "READY", "Listo"
    DELIVERED = "DELIVERED", "Entregado"
    PAID = "PAID", "Pagado"
    CANCELED = "CANCELED", "Cancelado"


class CourierStatus(models.TextChoices):
    ASSIGNED = "ASSIGNED", "Asignado"
    ON_ROUTE = "ON_ROUTE", "En camino"
    DELIVERED = "DELIVERED", "Entregado"


class KitchenStatus(models.TextChoices):
    QUEUED = "QUEUED", "En cola"
    PREPARING = "PREPARING", "Preparando"
    READY = "READY", "Listo"


class PaymentMethod(models.TextChoices):
    CASH = "CASH", "Efectivo"
    CARD = "CARD", "Tarjeta"
    TRANSFER = "TRANSFER", "Transferencia"


class InvoiceType(models.TextChoices):
    RECEIPT = "RECEIPT", "Boleta"
    INVOICE = "INVOICE", "Factura"
