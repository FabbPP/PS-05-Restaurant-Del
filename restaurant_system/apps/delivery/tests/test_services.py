import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.delivery.services import calculate_fee, assign_courier, update_delivery_status, EstadoInvalidoError
from apps.core.enums import OrderStatus

@pytest.mark.parametrize("distance, expected_fee", [
    (Decimal("0.00"), Decimal("5.00")), # AVL: Mínimo
    (Decimal("1.00"), Decimal("6.00")), # PE: Clase válida
    (Decimal("-1.00"), Decimal("5.00")),# Robustez: Negativo usa base fee
])
def test_calculate_fee_logic(distance, expected_fee):
    assert calculate_fee(distance) == expected_fee

def test_assign_inactive_courier(order_delivery, courier):
    """Test de excepción: Repartidor no disponible."""
    from apps.delivery.models import DeliveryInfo
    info = DeliveryInfo.objects.create(
        order=order_delivery, 
        address="Calle 1", 
        phone="123456789", 
        distance_km=Decimal("5.00"),
        estimated_time_min=40,
        delivery_fee=Decimal("10.00")
    )
    
    courier.is_available = False
    courier.save()
    
    from apps.delivery.services import RepartidorNoDisponibleError
    with pytest.raises(RepartidorNoDisponibleError):
        assign_courier(info, courier)

def test_delivery_fsm_protection(order_delivery, courier):
    """Test de validación: Protección de flujo de despacho."""
    from apps.delivery.models import DeliveryInfo
    info = DeliveryInfo.objects.create(
        order=order_delivery, 
        address="Calle 1", 
        phone="123456789", 
        distance_km=Decimal("5.00"),
        estimated_time_min=40,
        delivery_fee=Decimal("10.00")
    )
    
    # Intentar marcar como entregado sin estar en camino
    with pytest.raises(EstadoInvalidoError):
        update_delivery_status(info, OrderStatus.DELIVERED)
        
    # Flujo correcto
    update_delivery_status(info, OrderStatus.PREPARING)
    assign_courier(info, courier)
    update_delivery_status(info, OrderStatus.READY) # On Route
    update_delivery_status(info, OrderStatus.DELIVERED)
    
    assert order_delivery.status == OrderStatus.DELIVERED