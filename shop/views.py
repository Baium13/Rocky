import pycountry
from django.views import View

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from .models import *
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .order_service import OrderService
from .product_service import ProductService
from django.contrib.auth.views import LoginView, LogoutView


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
            {'all_products': all_products, 'total_items': order.total_items if order else 0}
        )
        return context


class BaseCartView(BaseView):
    template_name = 'shop/store.html'
    http_method_names = [
        "get",
        "post"
    ]

    def get_response(self):
        redirect_to = self.request.POST.get("redirect_to")
        if redirect_to:
            return redirect(redirect_to + f"?currency={self.request.POST.get('currency')}")
        return redirect(reverse("shop:store") + f"?currency={self.request.POST.get('currency')}")

    def post(self, request, *args, **kwargs):
        order = self.get_or_create_order()
        product = ProductService.get_product(request.POST.get('product_id'))

        if request.POST.get('action') == "add":
            order.add_product(product, request.POST.get('currency'))
            return self.get_response()
        elif request.POST.get('action') == "remove":
            order.remove_product(product, request.POST.get('currency'))
            return self.get_response()


class AddToCartView(BaseCartView):
    pass


class CartView(BaseCartView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            "order": self.get_or_create_order(),
            'total_items': self.get_or_create_order().total_items
        })
        return context


class OrderView(CartView):
    template_name = 'shop/checkout.html'
    http_method_names = [
        "get",
        "post"
    ]

    def get_response(self):
        return redirect(reverse("shop:place_order") + f"?currency={self.request.POST.get('currency')}")

    def post(self, request, *args, **kwargs):
        order = self.get_or_create_order()
        address_id = request.POST.get('address_id')
        if address_id:
            address = ShippingAddress.objects.get(id=address_id)
            order.add_address(address)
        else:
            email = request.POST.get('email')
            # first_name = request.POST.get('first_name')
            country = request.POST.get('country')
            get_code = pycountry.countries.get(name=country)
            code = get_code.alpha_2
            town = request.POST.get('town')
            line1 = request.POST.get('line1')
            line2 = request.POST.get('line2')
            postal_code = request.POST.get('postal_code')
            country_instance, created = Country.objects.get_or_create(name=country, code=code)
            order.add_address(country=country_instance,
                              town=town,
                              line1=line1,
                              line2=line2,
                              postal_code=postal_code)
            order.email = email
        order.status = OrderStatus.COMPLETED.value
        order.save()

        return self.get_response()


class PlaceOrderView(BaseView):
    template_name = 'shop/place_order.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            order_completed = OrderService.get_completed_order_by_user(self.request.user)
        elif self.request.session.get("order_id"):
            order_completed = OrderService.get_completed_order_by_id(self.request.session.get("order_id"))
        context = super().get_context_data()
        context.update({
            "order": order_completed,
            "total_items": order_completed.total_items,
            "shipping_addresses": OrderShippingAddress.objects.get(order_id=order_completed.id)
        })
        messages.success(self.request, 'Order Completed success.')
        return context


class CustomLoginView(LoginView):
    template_name = 'shop/login_form.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('shop:store')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class CustomRegistrationView(View):
    template_name = 'shop/registration.html'
    form_class = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:store')
        else:
            error_message = f"An error occurred during user creation: {form.error_messages}"
            messages.error(request, error_message)
        return render(request, self.template_name, {'form': form})


class CustomLogoutView(LogoutView):
    template_name = 'shop/logout_form.html'

    def get_response(self):
        return redirect(reverse("shop:logout_form") + f"?currency={self.request.POST.get('currency')}")
