import pytest
from django.core.exceptions import ValidationError

from apps.core.validators import validate_non_empty


def test_validate_non_empty():
    with pytest.raises(ValidationError):
        validate_non_empty("   ")
