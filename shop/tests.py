# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from shop.factories import OrderFactory, ProductFactory, ProductPriceFactory, OrderLineFactory, CountryFactory, \
    ShippingFactory, ShippingAddressFactory


class AddToCartTests(TestCase):

    def test_add_to_cart(self):
        # given
        order = OrderFactory()
        self.client.force_login(order.user)
        currency = 'USD'
        product = ProductFactory()
        expected_redirect_to = reverse('shop:store')
        ProductPriceFactory(product=product, currency=currency)
        # when
        response = self.client.post(reverse("shop:add-to-cart"), data={
            "action": "add",
            "redirect_to": expected_redirect_to,
            "currency": currency,
            "product_id": product.pk
        })
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expected_redirect_to + f"?currency={currency}", response.url)
        order_lines = order.orderline_set.count()
        self.assertEqual(order_lines, 1, f"Order should have 1 line, but got {order_lines}")


class RemoveFromCartTests(TestCase):
    def test_remove_from_cart(self):
        # given
        order = OrderFactory()
        self.client.force_login(order.user)
        product = ProductFactory()
        currency = 'USD'
        ProductPriceFactory(product=product, currency=currency)
        OrderLineFactory(order=order)
        expected_redirect_to = reverse('shop:cart')
        # when
        response = self.client.post(reverse("shop:remove-from-cart"), data={
            "action": "remove",
            "redirect_to": expected_redirect_to,
            "currency": currency,
            "product_upc": product.upc
        })
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expected_redirect_to + f"?currency={currency}", response.url)
        order_lines = order.orderline_set.count()
        self.assertEqual(order_lines, 0, f"Order should have 0 line, but got {order_lines}")


class AddFromCartTests(TestCase):
    def test_add_from_cart(self):
        # given
        order = OrderFactory()
        self.client.force_login(order.user)
        product = ProductFactory()
        currency = 'USD'
        ProductPriceFactory(product=product, currency=currency)
        product_in_line = OrderLineFactory(order=order)
        expected_redirect_to = reverse('shop:cart')
        # when
        response = self.client.post(reverse("shop:add-to-cart"), data={
            "action": "add",
            "redirect_to": expected_redirect_to,
            "currency": currency,
            "product_upc": product_in_line.upc
        })
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expected_redirect_to + f"?currency={currency}", response.url)
        updated_order_lines = order.orderline_set.count()
        self.assertEqual(updated_order_lines, 1, f"Expected 2 order lines, but got {updated_order_lines}")


class OrderStatusChangeTests(TestCase):
    def test_order_status_completed(self):
        # given
        order = OrderFactory()
        OrderLineFactory(order=order)
        self.client.force_login(order.user)
        currency = 'USD'
        expected_redirect_to = reverse('shop:place_order')
        address = ShippingAddressFactory()
        # when
        response = self.client.post(reverse("shop:checkout"), data={
            "address_id": address.id,
            "redirect_to": expected_redirect_to,
            "currency": currency,
        })
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expected_redirect_to + f"?currency={currency}", response.url)
        order.refresh_from_db()
        order_status = order.status
        self.assertEqual(order_status, 'completed',
                         f"Order should have status COMPLETED, but got {order_status}")
