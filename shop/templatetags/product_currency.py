from shop.models import Product, ProductPrice
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def product_price(context, product: Product):
    try:
        product_pr = product.get_price_by_currency(context['request'].session["currency"])
        return f"{product_pr.price} ({product_pr.currency})"
    except ProductPrice.DoesNotExist:
        return "Unavailable"


@register.simple_tag(takes_context=True)
def product_price_available(context, product: Product):
    try:
        return bool(product.get_price_by_currency(context['request'].session["currency"]))
    except ProductPrice.DoesNotExist:
        return False
