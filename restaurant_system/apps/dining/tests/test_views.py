def test_table_create_view(client):
    response = client.post("/dining/tables/create/", data={"number": 2, "capacity": 4, "status": "FREE"})
    assert response.status_code == 201
