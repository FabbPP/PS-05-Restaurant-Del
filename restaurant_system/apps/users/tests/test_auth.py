import pytest
from django.urls import reverse
from tests.factories import UserFactory

@pytest.mark.auth
def test_login_invalid_credentials(client):
    """PE: Intento de login con credenciales erróneas."""
    url = reverse('users:login')
    response = client.post(url, {"username": "wrong", "password": "wrongpassword"})
    assert response.status_code in [401, 200] # Depende si es API o Template
    if response.status_code == 200:
        assert "error" in response.content.decode().lower()

@pytest.mark.auth
def test_login_inactive_user(client, db):
    """PE: Usuario bloqueado o inactivo."""
    user = UserFactory(is_active=False)
    user.set_password("valid_pass")
    user.save()
    
    response = client.post(reverse('users:login'), {"username": user.username, "password": "valid_pass"})
    # El sistema debe rechazar el acceso a usuarios inactivos
    assert response.status_code != 302 # No debe redireccionar al dashboard

@pytest.mark.auth
@pytest.mark.parametrize("username, password", [
    ("", "pass123"),          # PE: Vacío
    ("admin", ""),            # PE: Vacío
    ("A" * 300, "pass123"),   # Robustez: Giant string
    ("admin' OR '1'='1", "p"),# Robustez: Intento inyección simple
])
def test_login_boundary_robustness(client, username, password):
    """AVL/Robustez: Campos de autenticación con valores límite."""
    response = client.post(reverse('users:login'), {
        "username": username,
        "password": password
    })
    assert response.status_code != 500 # El sistema nunca debe caerse