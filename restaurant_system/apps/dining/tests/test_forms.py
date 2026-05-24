from apps.dining.forms import TableForm


def test_table_form_invalid_capacity():
    form = TableForm(data={"number": 1, "capacity": 0, "status": "FREE"})
    assert not form.is_valid()
    assert "__all__" in form.errors
