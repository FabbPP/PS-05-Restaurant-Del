from __future__ import annotations

from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.delivery.models import DeliveryInfo, Courier
from apps.core.enums import OrderStatus, CourierStatus

BASE_FEE = Decimal("5.00")
PER_KM_FEE = Decimal("1.00")

class EstadoInvalidoError(Exception):
    """Lanzada para transiciones de estado no permitidas en el flujo logístico."""
    pass

class RepartidorNoDisponibleError(Exception):
    """Lanzada cuando un repartidor no puede tomar un pedido."""
    pass


def calculate_fee(distance_km: Decimal) -> Decimal:
    if distance_km < 0: return BASE_FEE
    return BASE_FEE + (PER_KM_FEE * distance_km)


def estimate_time(distance_km: Decimal) -> int:
    # Critical: keep deterministic for tests and avoid external dependencies.
    return int(max(5, min(180, distance_km * Decimal("8"))))


def update_delivery_cost(info: DeliveryInfo) -> DeliveryInfo:
    try:
        info.delivery_fee = calculate_fee(info.distance_km)
        info.estimated_time_min = estimate_time(info.distance_km)
        info.full_clean()
        info.save()
        return info
    except Exception as e:
        raise ValidationError(f"Error al actualizar costos de envío: {e}")

@transaction.atomic
def assign_courier(delivery_info: DeliveryInfo, courier: Courier) -> DeliveryInfo:
    """Asigna un repartidor validando disponibilidad y estado del pedido."""
    if not courier.is_available or not courier.user.is_active:
        raise RepartidorNoDisponibleError(f"El repartidor {courier.user.get_full_name()} no está disponible.")
    
    # Si el repartidor ya tiene un pedido ON_ROUTE, no permitir más (opcional según regla negocio)
    # if DeliveryInfo.objects.filter(courier=courier, courier_status=CourierStatus.ON_ROUTE).exists():
    #    raise RepartidorNoDisponibleError("El repartidor ya está en una entrega.")

    delivery_info.courier = courier
    delivery_info.courier_status = CourierStatus.ASSIGNED
    delivery_info.save()
    return delivery_info

@transaction.atomic
def update_delivery_status(delivery_info: DeliveryInfo, new_order_status: str) -> None:
    """
    FSM Estricta: Pendiente -> Preparando -> En Camino (READY) -> Entregado (DELIVERED).
    """
    order = delivery_info.order
    current = order.status

    # Definición de transiciones permitidas (FSM)
    allowed_transitions = {
        OrderStatus.PENDING: [OrderStatus.PREPARING, OrderStatus.CANCELED],
        OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELED],
        OrderStatus.READY: [OrderStatus.DELIVERED], # READY equivale a "En Camino" para delivery
        OrderStatus.DELIVERED: [OrderStatus.PAID],
    }

    if new_order_status not in allowed_transitions.get(current, []):
        raise EstadoInvalidoError(f"Transición ilegal: {current} -> {new_order_status}")

    # Reglas de negocio específicas del despacho
    if new_order_status == OrderStatus.READY and not delivery_info.courier:
        raise EstadoInvalidoError("No se puede poner en camino sin un repartidor asignado.")

    # Actualizar estados sincronizados
    order.status = new_order_status
    order.save()

    if new_order_status == OrderStatus.READY:
        delivery_info.courier_status = CourierStatus.ON_ROUTE
        if delivery_info.courier:
            delivery_info.courier.is_available = False
            delivery_info.courier.save()
    
    elif new_order_status == OrderStatus.DELIVERED:
        delivery_info.courier_status = CourierStatus.DELIVERED
        if delivery_info.courier:
            delivery_info.courier.is_available = True
            delivery_info.courier.save()

    delivery_info.save()
