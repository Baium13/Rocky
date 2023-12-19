from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.conf import settings

"""Check please """


class ShippingAddress(models.Model):
    country = CountryField()
    town = models.CharField(max_length=255)
    line1 = models.CharField(max_length=255, help_text='street address and building number')
    line2 = models.CharField(max_length=255, help_text='apt number')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


class OrderShippingAddress(models.Model):
    order_shipping_address = models.ForeignKey(ShippingAddress)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    numbers = models.IntegerField(default=0)
    date_created = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)
    total = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, default='USD')
    shipping_address = models.ForeignKey(OrderShippingAddress)
    shipping_date = models.DateField()


class OrderLine(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=False)
    quantity = models.IntegerField()
    line_price = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    sku = models.CharField(max_length=255, null=False)
    upc = models.IntegerField(max_length=12, null=False)
    description = models.CharField(max_length=255, null=True)


class Image(models.Model):
    url = models.URLField(max_length=255, null=False)
    alt_url = models.URLField(max_length=255, null=False)


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ManyToManyField(Image, blank=True)
    default_image = models.ImageField(upload_to='default_images/%Y/%m/%d/')


class Country(models.Model):
    name = models.CharField(max_length=255, null=False)
    code = models.CharField(max_length=15, null=False)


class ProductPrice(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    currency = models.CharField(max_length=3, default='USD', null=False)
    product = models.ForeignKey(Product)
    country = models.ForeignKey(Country)


class Category(models.Model):
    name = models.ManyToManyField(Product)
    description = models.CharField(max_length=255)
    image = models.ManyToManyField(Image, blank=True)
    default_image = models.ImageField(upload_to='default_images/%Y/%m/%d/')
