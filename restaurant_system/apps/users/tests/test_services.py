from apps.users.services import create_user


def test_create_user_service(db):
    user = create_user(username="service_user", password="pass12345!", role="ADMIN")
    assert user.id is not None
