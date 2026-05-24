import pytest
from django.core.exceptions import ValidationError

from apps.dining.models import Table


def test_table_capacity_invalid():
    table = Table(number=1, capacity=0)
    with pytest.raises(ValidationError):
        table.full_clean()
