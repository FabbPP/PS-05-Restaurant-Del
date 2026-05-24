def test_ticket_create_view(client, order_dine_in):
    response = client.post("/kitchen/create/", data={"order": order_dine_in.id, "status": "QUEUED"})
    assert response.status_code == 201
