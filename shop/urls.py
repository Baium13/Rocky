from django.urls import path
from . import views
from .views import AddToCartView, CartView

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("remove/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),

]
