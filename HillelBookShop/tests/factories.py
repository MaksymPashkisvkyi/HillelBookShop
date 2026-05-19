import decimal

import factory
from django.contrib.auth import get_user_model

from payments.models import Payment
from shop.models import Author, Category, Customer, Product
from shop.orders.models import Order, OrderItem

User = get_user_model()


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone = factory.Sequence(lambda n: f"+380000000{n:03d}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        raw_password = extracted or "password123"
        self.set_password(raw_password)
        if create:
            self.save(update_fields=["password"])


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")
    is_active = True


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f"Author {n}")
    slug = factory.Sequence(lambda n: f"author-{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(AuthorFactory)
    name = factory.Sequence(lambda n: f"Book {n}")
    slug = factory.Sequence(lambda n: f"book-{n}")
    description = factory.Faker("sentence")
    ISBN = factory.Sequence(lambda n: f"9780000000{n:03d}")
    price = decimal.Decimal("100.00")
    discount_price = None
    stock = 5
    image = factory.django.ImageField(color="blue")
    is_active = True


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserProfileFactory)
    address = factory.Faker("address")


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(UserProfileFactory)
    stripe_payment_intent_id = factory.Sequence(lambda n: f"pi_{n}")
    amount = decimal.Decimal("100.00")
    currency = "UAH"
    status = Payment.Status.PENDING
    description = "Test payment"
    metadata = factory.LazyFunction(dict)
    refund_amount = decimal.Decimal("0.00")


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    first_name = factory.LazyAttribute(lambda obj: obj.customer.user.first_name)
    last_name = factory.LazyAttribute(lambda obj: obj.customer.user.last_name)
    email = factory.LazyAttribute(lambda obj: obj.customer.user.email)
    phone = factory.LazyAttribute(lambda obj: obj.customer.user.phone)
    address = factory.LazyAttribute(lambda obj: obj.customer.address)
    status = Order.OrderStatus.CREATED
    total_price = decimal.Decimal("100.00")
    payment = None


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = decimal.Decimal("50.00")
    quantity = 2
