from django.urls import path
from . import views
from .views import AddToCartView, CartView, OrderView, PlaceOrderView, CustomLoginView, CustomRegistrationView, \
    CustomLogoutView

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='store'),
    path("cart/", CartView.as_view(), name="cart"),
    path("checkout/", OrderView.as_view(), name='checkout'),
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('login_form/', CustomLoginView.as_view(), name='login_form'),
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('logout_form/', CustomLogoutView.as_view(), name='logout_form'),
]
