from django import forms

from apps.core.validators import validate_non_empty


class DummyForm(forms.Form):
    name = forms.CharField(validators=[validate_non_empty])


def test_dummy_form_rejects_blank():
    form = DummyForm(data={"name": " "})
    assert not form.is_valid()
