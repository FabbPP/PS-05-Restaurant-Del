def test_user_create_view(client):
    response = client.post(
        "/users/create/",
        data={
            "username": "view_user",
            "password1": "pass12345!",
            "password2": "pass12345!",
            "role": "ADMIN",
            "phone": "999888777",
        },
    )
    assert response.status_code == 201
