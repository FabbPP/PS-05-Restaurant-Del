from apps.delivery.forms import DeliveryInfoForm


def test_delivery_form_invalid_distance(order_delivery):
    form = DeliveryInfoForm(
        data={
            "order": order_delivery.id,
            "address": "Av 1",
            "phone": "999888777",
            "distance_km": 20,
            "delivery_fee": 0,
            "estimated_time_min": 10,
        }
    )
    assert not form.is_valid()
    assert "distance_km" in form.errors
