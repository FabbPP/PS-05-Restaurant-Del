def test_delivery_create_view(client, order_delivery):
    response = client.post(
        "/delivery/create/",
        data={
            "order": order_delivery.id,
            "address": "Av 1",
            "phone": "999888777",
            "distance_km": 5,
            "delivery_fee": 0,
            "estimated_time_min": 10,
        },
    )
    assert response.status_code == 201
