import pytest
from django.core.exceptions import ValidationError

from apps.users.models import User


def test_user_phone_invalid():
    user = User(username="u1", phone="abc", role="ADMIN")
    with pytest.raises(ValidationError):
        user.full_clean()
