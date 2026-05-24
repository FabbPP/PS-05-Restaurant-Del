def test_customer_create_view(client):
    response = client.post(
        "/customers/create/",
        data={"name": "Ana", "email": "ana@example.com", "phone": "999888777"},
    )
    assert response.status_code == 201
