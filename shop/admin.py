from django.contrib import admin
from .models import *


class ShippingAddressAdmin(admin.TabularInline):
    model = ShippingAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ShippingAddressAdmin]
    pass


class ProductPriceAdmin(admin.TabularInline):
    model = ProductPrice


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPriceAdmin]
    list_display = ['name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class OrderShippingAddressAdmin(admin.TabularInline):
    model = OrderShippingAddress


class OrderLineAdmin(admin.TabularInline):
    model = OrderLine


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineAdmin, OrderShippingAddressAdmin]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
