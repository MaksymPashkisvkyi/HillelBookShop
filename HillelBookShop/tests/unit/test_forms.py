import pytest

from accounts.forms import LoginForm, ProfileForm, RegistrationForm
from shop.orders.forms import OrderCreateForm


@pytest.mark.django_db
def test_registration_form_saves_hashed_password():
    form = RegistrationForm(
        data={
            "email": "new@example.com",
            "phone": "+380123123123",
            "first_name": "New",
            "last_name": "User",
            "password1": "secret123",
            "password2": "secret123",
        }
    )

    assert form.is_valid(), form.errors
    user = form.save()

    assert user.check_password("secret123") is True
    assert user.password != "secret123"


@pytest.mark.django_db
def test_registration_form_rejects_password_mismatch():
    form = RegistrationForm(
        data={
            "email": "new@example.com",
            "phone": "+380123123123",
            "first_name": "New",
            "last_name": "User",
            "password1": "secret123",
            "password2": "different123",
        }
    )

    assert form.is_valid() is False
    assert "Passwords don't match" in form.non_field_errors()


def test_registration_form_sets_expected_placeholders():
    form = RegistrationForm()
    assert form.fields["first_name"].widget.attrs["placeholder"] == "Type here"
    assert form.fields["email"].widget.attrs["placeholder"] == "Enter email address"
    assert form.fields["password1"].widget.attrs["placeholder"] == "Enter password"


def test_login_form_sets_expected_placeholders():
    form = LoginForm()
    assert form.fields["username"].widget.attrs["placeholder"] == "Enter email"
    assert form.fields["password"].widget.attrs["placeholder"] == "Enter your password"


def test_profile_form_uses_date_input_and_placeholders():
    form = ProfileForm()
    assert form.fields["date_of_birth"].widget.input_type == "date"
    assert form.fields["first_name"].widget.attrs["placeholder"] == "Enter first name"
    assert form.fields["phone"].widget.attrs["placeholder"] == "Enter phone number"


def test_order_create_form_sets_placeholders_and_textarea_attrs():
    form = OrderCreateForm()
    assert form.fields["first_name"].widget.attrs["placeholder"] == "First name"
    assert form.fields["address"].widget.attrs["placeholder"] == "City, street, building"
    assert form.fields["address"].widget.attrs["rows"] == 3
