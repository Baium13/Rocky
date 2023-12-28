from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.conf import settings

from Rocky.enum import Currency, OrderStatus


class AbstractAuditableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class AbstractShippingAddress(AbstractAuditableModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = CountryField()
    town = models.CharField(max_length=255)
    line1 = models.CharField(max_length=255, help_text='street address and building number')
    line2 = models.CharField(max_length=255, help_text='apt number')
    postal_code = models.CharField(max_length=50, help_text='postal code')

    class Meta:
        abstract = True


class ShippingAddress(AbstractShippingAddress):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


class OrderShippingAddress(AbstractShippingAddress):
    pass


class Order(AbstractAuditableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.CharField(max_length=50, help_text='order number')
    status = models.CharField(max_length=50, choices=OrderStatus.choices())
    total = models.DecimalField("Order total", max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices())
    shipping_address = models.ForeignKey(OrderShippingAddress, null=True, on_delete=models.SET_NULL)
    shipping_date = models.DateField()


class OrderLine(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=False)
    quantity = models.PositiveIntegerField()
    line_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    sku = models.CharField(max_length=50)
    upc = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)


class ProductImage(AbstractAuditableModel):
    image = models.ImageField()
    alt_text = models.CharField(max_length=255, null=True)


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    images = models.ManyToManyField(ProductImage, related_name="products")
    default_image = models.ImageField(null=True)


class ProductPrice(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    currency = models.CharField(max_length=3, choices=Currency.choices())
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    country = CountryField()


class Category(models.Model):
    name = models.ManyToManyField(Product)
    description = models.CharField(max_length=255)
    default_image = models.ImageField(null=True)
