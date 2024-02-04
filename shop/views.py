from django.contrib import messages
from django.urls import reverse

from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .order_service import OrderService
from .product_service import ProductService


class BaseView(TemplateView):
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('currency'):
            self.request.session["currency"] = self.request.GET.get('currency')
        elif not self.request.session.get('currency'):
            self.request.session['currency'] = Currency.USD.value
        return super().dispatch(*args, **kwargs)

    def get_or_create_order(self) -> Order:
        if self.request.user.is_authenticated:
            order = OrderService.get_pending_order_by_user(self.request.user)
            if not order:
                order = OrderService.create_pending_order(
                    currency=self.request.session.get("currency"),
                    user=self.request.user
                )
        elif self.request.session.get("order_id"):
            order = OrderService.get_pending_order_by_id(self.request.session.get("order_id"))
        else:
            order = OrderService.create_pending_order(
                currency=self.request.session.get("currency"),
            )
            self.request.session["order_id"] = order.pk
        return order


class ProductListView(BaseView):
    template_name = 'shop/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = None
        if self.request.user.is_authenticated:
            order = OrderService.get_pending_order_by_user(self.request.user)
        elif self.request.session.get("order_id"):
            order = OrderService.get_pending_order_by_id(self.request.session.get("order_id"))
        all_products = ProductService.get_all_products()
        context.update(
            {'all_products': all_products, 'total_item': order.total_items if order else 0}
        )
        return context


class BaseCartView(BaseView):
    template_name = 'shop/store.html'
    http_method_names = [
        "get",
        "post"
    ]

    def get_response(self):
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        """
        This is add to cart functionality
        """
        order = self.get_or_create_order()
        product = ProductService.get_product(request.POST.get('product_id'))

        if request.POST.get('action') == "add":
            order.add_product(product, request.POST.get('currency'))
        elif request.POST.get('action') == "remove":
            order.remove_product(product, request.POST.get('currency'))
        return self.get_response()


class AddToCartView(BaseCartView):
    def get_response(self):
        redirect(reverse("shop:store") + f"?currency={self.request.POST.get('currency')}")


class CartView(BaseCartView):
    template_name = 'shop/cart.html'

    def get_response(self):
        redirect(reverse("shop:cart") + f"?currency={self.request.POST.get('currency')}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            "order": self.get_or_create_order()
        })
        return context

@login_required
def add_to_cart(request, id_product):
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    product = get_object_or_404(Product, id=id_product)
    image = product.default_image
    product_price_item = get_object_or_404(ProductPrice, product_id=id_product)
    if created is True:
        order.user = request.user
        order.number = 1
        order.currency = product_price_item.currency
        order.status = 'pending'

    cart_item_product_list = OrderLine.objects.filter(order=order, upc=product.upc).first()
    cart_item_order_line = OrderLine.objects.filter(order=order, upc=id_product).first()
    if cart_item_product_list or cart_item_order_line:
        cart_item_product_list.quantity += 1
        cart_item_product_list.save()
        return redirect("shop:cart")
    else:
        OrderLine.objects.create(order=order, product_name=product_price_item.product.name,
                                 item_price=product_price_item.price, quantity=1, default_image=image, upc=product.upc,
                                 sku=product.sku, description=product.description)
    order.recalculate_total()
    return redirect("shop:store")


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item_order_line = get_object_or_404(OrderLine, id=cart_item_id)
    order = cart_item_order_line.order
    if cart_item_order_line:
        cart_item_order_line.quantity -= 1
        cart_item_order_line.save()
        order.recalculate_total()
        if cart_item_order_line.quantity == 0:
            cart_item_order_line.delete()
    return redirect("shop:cart")


def cart(request):
    if request.user.is_authenticated and Order.objects.filter(user=request.user, status='pending').exists():
        order_item = get_object_or_404(Order, user=request.user, status='pending')
        cart_items = OrderLine.objects.filter(order__user=request.user, order__status='pending')
        total_item = sum(item.quantity for item in cart_items)
    else:
        order_item = []
        cart_items = []
        total_item = '0'
    context = {
        'order_item': order_item,
        "cart_items": cart_items,
        "total_item": total_item,
    }
    return render(request, "shop/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status='pending')
        shipping_addresses = ShippingAddress.objects.filter(user=request.user)
        items = order.orderline_set.all()
        total_item = sum(item.quantity for item in items)
    else:
        order = []
        shipping_addresses = []
        items = []
        total_item = 0
    context = {'order': order, 'items': items, 'total_item': total_item, 'shipping_addresses': shipping_addresses}
    return render(request, 'shop/checkout.html', context)


def place_order(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            address_id = request.POST.get('address_id')
            country = request.POST.get('country')
            code = country[0:2]
            town = request.POST.get('town')
            line1 = request.POST.get('line1')
            line2 = request.POST.get('line2')
            postal_code = request.POST.get('postal_code')

            if address_id:
                address = get_object_or_404(ShippingAddress, id=address_id)
                shipping_addresses = OrderShippingAddress.objects.create(country=address.country, town=address.town,
                                                                         line1=address.line1,
                                                                         line2=address.line2,
                                                                         postal_code=address.postal_code)
                shipping_addresses.save()
                order = get_object_or_404(Order, user=request.user, status='pending')
                order.status = 'completed'
                order.save()
                order_line = OrderLine.objects.filter(order__user=request.user, order__status='completed')
                total_item = sum(item.quantity for item in order_line)
                context = {'order_line': order_line, 'shipping_addresses': shipping_addresses, 'order': order,
                           'total_item': total_item}
                messages.success(request, 'Order Completed success.')
                return render(request, 'shop/place_order.html', context)

            else:
                country_instance, created = Country.objects.get_or_create(name=country, code=code)
                shipping_addresses = OrderShippingAddress.objects.create(country=country_instance, town=town,
                                                                         line1=line1,
                                                                         line2=line2,
                                                                         postal_code=postal_code)
                shipping_addresses.save()
                order = get_object_or_404(Order, user=request.user, status='pending')
                order.status = 'completed'
                order.save()
                order_line = OrderLine.objects.filter(order__user=request.user, order__status='completed')
                total_item = sum(item.quantity for item in order_line)
                context = {'order_line': order_line, 'shipping_addresses': shipping_addresses, 'order': order,
                           'total_item': total_item}
                messages.success(request, 'Order Completed success, and your new address has been placed.')
                return render(request, 'shop/place_order.html', context)

        order_line = []
        shipping_addresses = []
        context = {'order_line': order_line, 'shipping_addresses': shipping_addresses}
        return render(request, 'shop/place_order.html', context)
