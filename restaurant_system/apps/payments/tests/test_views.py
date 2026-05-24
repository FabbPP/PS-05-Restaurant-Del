def test_payment_create_view(client, order_dine_in):
    order_dine_in.total = 10
    order_dine_in.save()
    response = client.post(
        "/payments/create/",
        data={"order": order_dine_in.id, "method": "CASH", "amount": 10},
    )
    assert response.status_code == 201
