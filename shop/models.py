from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.conf import settings

from .enum import Currency, OrderStatus


class AbstractAuditableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class AbstractShippingAddress(AbstractAuditableModel):
    country = models.ForeignKey("shop.Country", on_delete=models.SET_NULL, null=True)
    town = models.CharField(max_length=255)
    line1 = models.CharField(max_length=255, help_text='street address and building number')
    line2 = models.CharField(max_length=255, help_text='apt number')
    postal_code = models.CharField(max_length=50, help_text='postal code')

    class Meta:
        abstract = True


class ShippingAddress(AbstractShippingAddress):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.line1},{self.line2}, {self.postal_code}, {self.country}"


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class OrderShippingAddress(AbstractShippingAddress):
    order = models.OneToOneField('shop.Order', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.country.code} / {self.postal_code}"


class Order(AbstractAuditableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.CharField(max_length=50, help_text='order number')
    status = models.CharField(max_length=50, choices=OrderStatus.choices())
    total = models.DecimalField("Order total", max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices())
    shipping_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.number}"

    def recalculate_total(self):
        self.total = self.orderline_set.all().aggregate(Sum('line_price'))['line_price__sum']
        self.save()


class ProductImage(AbstractAuditableModel):
    image = models.ImageField()
    alt_text = models.CharField(max_length=255, null=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    images = models.ManyToManyField(ProductImage, related_name="products")
    default_image = models.ImageField(null=True)
    upc = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=False)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    line_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    sku = models.CharField(max_length=50)
    upc = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)
    default_image = models.ImageField(null=True)

    def save(self, *args, **kwargs):
        self.line_price = self.item_price * self.quantity
        super().save(*args, **kwargs)


class ProductPrice(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices())
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    country = models.ForeignKey("shop.Country", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"({self.price}{self.currency})"


class Category(models.Model):
    name = models.CharField(max_length=255)
    product = models.ManyToManyField(Product)
    description = models.CharField(max_length=255)
    default_image = models.ImageField(null=True)

    def __str__(self):
        return f"{self.name}"


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.code
