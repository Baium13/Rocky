from django.contrib import admin
from .models import *


class ShippingAddressAdmin(admin.TabularInline):
    model = ShippingAddress


class OrderAdmin(admin.TabularInline):
    model = Order


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ShippingAddressAdmin, OrderAdmin]


class ProductPriceAdmin(admin.TabularInline):
    model = ProductPrice


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPriceAdmin]


class OrderLineAdmin(admin.ModelAdmin):
    pass


class CountryAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class OrderShippingAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(OrderShippingAddress, OrderShippingAddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Country, CountryAdmin)
