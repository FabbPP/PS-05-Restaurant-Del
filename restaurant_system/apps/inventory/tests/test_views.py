def test_stock_create_view(client, product):
    response = client.post(
        "/inventory/stock/create/",
        data={"product": product.id, "quantity": 5, "low_stock_threshold": 1},
    )
    assert response.status_code == 201
