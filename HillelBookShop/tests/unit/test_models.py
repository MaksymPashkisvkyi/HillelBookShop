import decimal

import pytest

from payments.models import Payment
from tests.factories import CustomerFactory, OrderItemFactory, PaymentFactory, ProductFactory, UserProfileFactory


@pytest.mark.django_db
def test_create_user_requires_email():
    # Generated with AI, reviewed and modified
    with pytest.raises(ValueError, match="Email address"):
        UserProfileFactory._meta.model.objects.create_user(email="", phone="+380111111111")


@pytest.mark.django_db
def test_create_user_requires_phone():
    # Generated with AI, reviewed and modified
    with pytest.raises(ValueError, match="Phone number"):
        UserProfileFactory._meta.model.objects.create_user(email="user@example.com", phone="")


@pytest.mark.django_db
def test_create_superuser_sets_flags():
    # Generated with AI, reviewed and modified
    user = UserProfileFactory._meta.model.objects.create_superuser(
        email="admin@example.com",
        phone="+380999999999",
        password="secret123",
    )

    assert user.is_staff is True
    assert user.is_superuser is True


@pytest.mark.django_db
def test_create_superuser_requires_staff_flag():
    # Generated with AI, reviewed and modified
    with pytest.raises(ValueError, match="is_staff=True"):
        UserProfileFactory._meta.model.objects.create_superuser(
            email="admin2@example.com",
            phone="+380999999998",
            password="secret123",
            is_staff=False,
        )


@pytest.mark.django_db
def test_user_get_full_name():
    # Generated with AI, reviewed and modified
    user = UserProfileFactory(first_name="Ada", last_name="Lovelace")
    assert user.get_full_name() == "Ada Lovelace"


@pytest.mark.django_db
def test_product_current_price_uses_discount_price():
    # Generated with AI, reviewed and modified
    product = ProductFactory(price=decimal.Decimal("200.00"), discount_price=decimal.Decimal("150.00"))
    assert product.current_price == decimal.Decimal("150.00")


@pytest.mark.django_db
def test_product_current_price_falls_back_to_regular_price():
    # Generated with AI, reviewed and modified
    product = ProductFactory(price=decimal.Decimal("200.00"), discount_price=None)
    assert product.current_price == decimal.Decimal("200.00")


@pytest.mark.django_db
def test_product_active_manager_returns_only_active_in_stock_products():
    # Generated with AI, reviewed and modified
    active_product = ProductFactory(is_active=True, stock=3)
    ProductFactory(is_active=False, stock=3)
    ProductFactory(is_active=True, stock=0)

    assert list(active_product.__class__.active.all()) == [active_product]


@pytest.mark.django_db
def test_customer_string_prefers_full_name():
    # Generated with AI, reviewed and modified
    customer = CustomerFactory(user__first_name="Grace", user__last_name="Hopper")
    assert str(customer) == "Grace Hopper"


@pytest.mark.django_db
def test_customer_string_falls_back_to_email():
    # Generated with AI, reviewed and modified
    customer = CustomerFactory(user__first_name="", user__last_name="", user__email="fallback@example.com")
    assert str(customer) == "fallback@example.com"


@pytest.mark.django_db
def test_order_item_get_total():
    # Generated with AI, reviewed and modified
    item = OrderItemFactory(price=decimal.Decimal("19.99"), quantity=3)
    assert item.get_total() == decimal.Decimal("59.97")


@pytest.mark.django_db
def test_payment_is_successful_property():
    # Generated with AI, reviewed and modified
    payment = PaymentFactory(status=Payment.Status.SUCCEEDED)
    assert payment.is_successful is True


@pytest.mark.django_db
def test_payment_can_be_refunded_when_successful_and_not_over_refunded():
    # Generated with AI, reviewed and modified
    payment = PaymentFactory(
        status=Payment.Status.SUCCEEDED,
        amount=decimal.Decimal("100.00"),
        refund_amount=decimal.Decimal("20.00"),
    )
    assert payment.can_be_refunded is True


@pytest.mark.django_db
def test_payment_cannot_be_refunded_when_not_successful():
    # Generated with AI, reviewed and modified
    payment = PaymentFactory(status=Payment.Status.PENDING)
    assert payment.can_be_refunded is False


@pytest.mark.django_db
def test_payment_cannot_be_refunded_when_refund_exceeds_amount():
    # Generated with AI, reviewed and modified
    payment = PaymentFactory(
        status=Payment.Status.SUCCEEDED,
        amount=decimal.Decimal("50.00"),
        refund_amount=decimal.Decimal("55.00"),
    )
    assert payment.can_be_refunded is False
