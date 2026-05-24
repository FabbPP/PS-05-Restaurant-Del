from apps.users.forms import UserRegisterForm


def test_user_register_form_invalid_phone():
    form = UserRegisterForm(
        data={
            "username": "u1",
            "password1": "pass12345!",
            "password2": "pass12345!",
            "role": "ADMIN",
            "phone": "abc",
        }
    )
    assert not form.is_valid()
    assert "phone" in form.errors
