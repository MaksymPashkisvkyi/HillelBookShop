from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from payments.models import Payment
from tests.factories import CategoryFactory, CustomerFactory, OrderFactory, PaymentFactory, ProductFactory, UserProfileFactory


@pytest.mark.django_db
def test_register_page_loads(client):
    # Generated with AI, reviewed and modified
    response = client.get(reverse("register"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_flow_creates_user_and_redirects_to_login(client):
    # Generated with AI, reviewed and modified
    response = client.post(
        reverse("register"),
        {
            "email": "flow@example.com",
            "phone": "+380555555555",
            "first_name": "Flow",
            "last_name": "User",
            "password1": "secret123",
            "password2": "secret123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("login")


@pytest.mark.django_db
def test_login_flow_redirects_authenticated_user(client):
    # Generated with AI, reviewed and modified
    user = UserProfileFactory()
    response = client.post(reverse("login"), {"username": user.email, "password": "password123"})
    assert response.status_code == 302
    assert response.url == reverse("profile")


@pytest.mark.django_db
def test_profile_requires_login(client):
    # Generated with AI, reviewed and modified
    response = client.get(reverse("profile"))
    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_authenticated_user_can_open_profile_page(client):
    # Generated with AI, reviewed and modified
    user = UserProfileFactory()
    client.force_login(user)
    response = client.get(reverse("profile"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_update_flow_updates_user_fields(client):
    # Generated with AI, reviewed and modified
    user = UserProfileFactory()
    client.force_login(user)

    response = client.post(
        reverse("profile"),
        {
            "first_name": "Updated",
            "last_name": "Name",
            "email": user.email,
            "phone": user.phone,
            "date_of_birth": "2000-01-01",
        },
    )

    user.refresh_from_db()
    assert response.status_code == 302
    assert user.first_name == "Updated"
    assert str(user.date_of_birth) == "2000-01-01"


@pytest.mark.django_db
def test_shop_home_page_renders_products(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory()
    response = client.get(reverse("shop"))
    assert response.status_code == 200
    assert product.name in response.content.decode()


@pytest.mark.django_db
def test_shop_filter_by_category_returns_filtered_products(client):
    # Generated with AI, reviewed and modified
    category = CategoryFactory()
    included = ProductFactory(category=category, name="Included book")
    ProductFactory(name="Excluded book")

    response = client.get(reverse("shop"), {"category": [category.id]})

    content = response.content.decode()
    assert response.status_code == 200
    assert included.name in content
    assert "Excluded book" not in content


@pytest.mark.django_db
def test_product_detail_page_renders(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory()
    response = client.get(reverse("product_detail", args=[product.slug]))
    assert response.status_code == 200
    assert product.name in response.content.decode()


@pytest.mark.django_db
def test_cart_add_flow_stores_product_in_session(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory()
    response = client.post(reverse("cart_add", args=[product.id]), {"quantity": 2})
    assert response.status_code == 302
    assert str(product.id) in client.session["cart"]
    assert client.session["cart"][str(product.id)]["quantity"] == 2


@pytest.mark.django_db
def test_cart_update_flow_changes_quantity(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory()
    client.post(reverse("cart_add", args=[product.id]), {"quantity": 1})

    response = client.post(reverse("cart_update", args=[product.id]), {"quantity": 5})

    assert response.status_code == 302
    assert client.session["cart"][str(product.id)]["quantity"] == 5


@pytest.mark.django_db
def test_cart_remove_flow_deletes_product(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory()
    client.post(reverse("cart_add", args=[product.id]), {"quantity": 1})

    response = client.get(reverse("cart_remove", args=[product.id]))

    assert response.status_code == 302
    assert str(product.id) not in client.session.get("cart", {})


@pytest.mark.django_db
def test_cart_clear_flow_empties_cart(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory()
    client.post(reverse("cart_add", args=[product.id]), {"quantity": 1})

    response = client.get(reverse("cart_clear"))

    assert response.status_code == 302
    assert client.session.get("cart", {}) == {}


@pytest.mark.django_db
def test_order_create_get_prefills_authenticated_user_data(client):
    # Generated with AI, reviewed and modified
    customer = CustomerFactory(address="Kyiv address")
    client.force_login(customer.user)
    product = ProductFactory()
    client.post(reverse("cart_add", args=[product.id]), {"quantity": 1})

    response = client.get(reverse("order_create"))

    assert response.status_code == 200
    assert response.context["form"]["address"].value() == "Kyiv address"


@pytest.mark.django_db
def test_order_create_post_creates_order_and_redirects_to_checkout(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory(price="120.00")
    client.post(reverse("cart_add", args=[product.id]), {"quantity": 2})

    response = client.post(
        reverse("order_create"),
        {
            "first_name": "Jane",
            "last_name": "Buyer",
            "email": "buyer@example.com",
            "phone": "+380111111111",
            "address": "Somewhere 1",
        },
    )

    assert response.status_code == 302
    assert "/checkout/" in response.url


@pytest.mark.django_db
def test_checkout_page_renders_for_existing_order(client):
    # Generated with AI, reviewed and modified
    order = OrderFactory()
    response = client.get(reverse("checkout_order", args=[order.id]))
    assert response.status_code == 200
    assert str(order.id).encode() in response.content


@pytest.mark.django_db
@patch("payments.views.StripePaymentService.create_payment_intent")
def test_create_payment_intent_api_flow(mock_create, api_client):
    # Generated with AI, reviewed and modified
    user = UserProfileFactory()
    payment = PaymentFactory(user=user, stripe_payment_intent_id="pi_777")
    mock_create.return_value = (payment, SimpleNamespace(client_secret="secret_777"))
    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse("payments:payment-create-payment-intent"),
        {"amount": "100.00", "currency": "usd", "description": "Checkout"},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["client_secret"] == "secret_777"


@pytest.mark.django_db
@patch("payments.views.send_receipt")
@patch("payments.views.StripePaymentService.confirm_payment")
def test_payment_confirm_flow(mock_confirm, mock_send_receipt, api_client):
    # Generated with AI, reviewed and modified
    payment = PaymentFactory(status=Payment.Status.PENDING)
    order = OrderFactory(payment=None, customer__user=payment.user)
    mock_confirm.return_value = payment
    api_client.force_authenticate(user=payment.user)

    response = api_client.post(
        reverse("payments:payment-confirm", args=[payment.id]),
        {"order_id": order.id},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    mock_send_receipt.assert_called_once()


@pytest.mark.django_db
def test_about_page_loads(client):
    # Generated with AI, reviewed and modified
    response = client.get(reverse("about"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_api_returns_only_active_root_categories(api_client):
    # Generated with AI, reviewed and modified
    active_root = CategoryFactory(parent=None, is_active=True, name="Active Root")
    CategoryFactory(parent=active_root, is_active=True, name="Child")
    CategoryFactory(parent=None, is_active=False, name="Inactive Root")

    response = api_client.get("/api/categories/")

    names = [item["name"] for item in response.data["results"]]
    assert response.status_code == status.HTTP_200_OK
    assert names == ["Active Root"]


@pytest.mark.django_db
def test_product_api_retrieve_by_slug_returns_product(api_client):
    # Generated with AI, reviewed and modified
    product = ProductFactory()

    response = api_client.get(f"/api/products/{product.slug}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == product.name
