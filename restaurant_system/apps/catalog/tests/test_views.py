def test_category_create_view(client):
    response = client.post("/catalog/categories/create/", data={"name": "Bebidas"})
    assert response.status_code == 201
