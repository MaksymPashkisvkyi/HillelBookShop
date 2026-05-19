from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status

from payments.models import Payment
from payments.stripe_service import StripePaymentService
from payments.utils import send_receipt
from tests.factories import OrderFactory, PaymentFactory, ProductFactory, UserProfileFactory


@pytest.mark.django_db
def test_checkout_view_returns_404_for_missing_order(client):
    # Generated with AI, reviewed and modified
    response = client.get(reverse("checkout_order", args=[999999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_product_detail_returns_404_for_missing_product(client):
    # Generated with AI, reviewed and modified
    response = client.get(reverse("product_detail", args=["missing-slug"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_send_receipt_sends_email():
    # Generated with AI, reviewed and modified
    order = OrderFactory(email="buyer@example.com")

    send_receipt(order)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["buyer@example.com"]
    assert str(order.id) in mail.outbox[0].subject


@pytest.mark.django_db
def test_create_payment_intent_raises_for_too_small_amount():
    # Generated with AI, reviewed and modified
    user = UserProfileFactory()

    with pytest.raises(ValueError, match="Minimum payment amount is 0.50"):
        StripePaymentService.create_payment_intent(user=user, amount=0.49)


@pytest.mark.django_db
@patch("payments.stripe_service.stripe.PaymentIntent.create")
def test_create_payment_intent_creates_local_payment_record(mock_create):
    # Generated with AI, reviewed and modified
    mock_create.return_value = SimpleNamespace(id="pi_test", client_secret="secret")
    user = UserProfileFactory()

    payment, payment_intent = StripePaymentService.create_payment_intent(
        user=user,
        amount=50,
        currency="usd",
        description="Book order",
    )

    assert payment.user == user
    assert payment.stripe_payment_intent_id == "pi_test"
    assert payment.currency == "USD"
    assert payment_intent.client_secret == "secret"


@pytest.mark.django_db
@patch("payments.stripe_service.stripe.PaymentIntent.retrieve")
def test_confirm_payment_marks_payment_successful(mock_retrieve):
    # Generated with AI, reviewed and modified
    mock_retrieve.return_value = SimpleNamespace(status=Payment.Status.SUCCEEDED, latest_charge="ch_123")
    payment = PaymentFactory(status=Payment.Status.PENDING)

    result = StripePaymentService.confirm_payment(
        payment_id=str(payment.id),
        stripe_payment_intent_id=payment.stripe_payment_intent_id,
    )

    payment.refresh_from_db()
    assert result.status == Payment.Status.SUCCEEDED
    assert payment.stripe_charge_id == "ch_123"


@pytest.mark.django_db
def test_product_detail_page_renders_product_name(client):
    # Generated with AI, reviewed and modified
    product = ProductFactory(name="Pragmatic Programmer")
    response = client.get(reverse("product_detail", args=[product.slug]))
    assert response.status_code == 200
    assert "Pragmatic Programmer" in response.content.decode()


@pytest.mark.django_db
def test_checkout_view_renders_existing_order(client):
    # Generated with AI, reviewed and modified
    order = OrderFactory()
    response = client.get(reverse("checkout_order", args=[order.id]))
    assert response.status_code == 200
    assert str(order.id) in response.content.decode()


@pytest.mark.django_db
@patch("payments.views.StripePaymentService.create_payment_intent")
def test_create_payment_intent_view_returns_400_on_value_error(mock_create, api_client):
    # Generated with AI, reviewed and modified
    user = UserProfileFactory()
    api_client.force_authenticate(user=user)
    mock_create.side_effect = ValueError("Bad payment")

    response = api_client.post(
        reverse("payments:payment-create-payment-intent"),
        {"amount": "100.00", "currency": "usd", "description": "Test"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Bad payment"


@pytest.mark.django_db
def test_confirm_view_requires_order_id(api_client):
    # Generated with AI, reviewed and modified
    payment = PaymentFactory()
    api_client.force_authenticate(user=payment.user)

    response = api_client.post(
        reverse("payments:payment-confirm", args=[payment.id]),
        {},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "order_id" in response.data["error"]


@pytest.mark.django_db
@patch("payments.views.send_receipt")
@patch("payments.views.StripePaymentService.confirm_payment")
def test_confirm_view_links_order_and_returns_serialized_payment(mock_confirm, mock_send_receipt, api_client):
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

    order.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert order.payment == payment
    mock_send_receipt.assert_called_once_with(order)
