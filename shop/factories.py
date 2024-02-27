import factory
from factory.django import DjangoModelFactory
from . import models
from .enum import OrderStatus


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User


class AnonymousOrderFactory(DjangoModelFactory):
    number = factory.Sequence(lambda n: f'order-{n}')
    user = None
    email = factory.Faker("email")
    status = OrderStatus.PENDING.value
    currency = 'USD'

    class Meta:
        model = models.Order


class OrderFactory(AnonymousOrderFactory):
    user = factory.SubFactory(UserFactory, username=factory.Sequence(lambda n: f'user{n}'))
    email = None

    class Meta:
        model = models.Order


class ProductFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f'product-{n}')
    description = factory.Sequence(lambda n: f'product-description-{n}')
    size = factory.Sequence(lambda n: f'product-size-{n}')
    weight = 12
    upc = factory.Sequence(lambda n: n)
    sku = factory.Sequence(lambda n: f'sku-{n}')

    class Meta:
        model = models.Product


class ProductPriceFactory(DjangoModelFactory):
    price = 12.00
    product = factory.SubFactory(ProductFactory)
    currency = 'USD'
    country = factory.SubFactory('shop.factories.CountryFactory')

    class Meta:
        model = models.ProductPrice


class CountryFactory(DjangoModelFactory):
    name = factory.Faker("country")
    code = factory.Faker("country")

    class Meta:
        model = models.Country


class OrderLineFactory(DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    product_name = factory.Sequence(lambda n: f'product-{n}')
    quantity = 1
    item_price = 2.50
    line_price = 2.50
    upc = factory.Sequence(lambda n: n)
    sku = factory.Sequence(lambda n: f'sku-{n}')

    class Meta:
        model = models.OrderLine


class ShippingFactory(DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    town = factory.Faker("city")
    line1 = factory.Faker("street_address")
    line2 = "apt 16"
    postal_code = factory.Faker("postcode")

    class Meta:
        abstract = True


class ShippingAddressFactory(ShippingFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.ShippingAddress


class OrderShippingAddressFactory(ShippingFactory):
    order = factory.SubFactory(OrderFactory)

    class Meta:
        model = models.OrderShippingAddress
