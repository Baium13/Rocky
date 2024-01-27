from .models import *
from django.shortcuts import render
from django.http import JsonResponse
import json


def store(request):
    products = Product.objects.all()
    prices = ProductPrice.objects.all()
    context = {'products': products, 'prices': prices}
    return render(request, 'shop/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer)
        items = order.orderline_set.all()
    else:
        items = []
        order = {'get_all_item': 0, 'total': 0}
    context = {'order': order, 'items': items}
    return render(request, 'shop/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer)
        items = order.orderline_set.all()
    else:
        items = []
        order = {'get_all_item': 0, 'total': 0}
    context = {'order': order, 'items': items}
    return render(request, 'shop/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    print('action:', action)
    print('product_id:', product_id)
    customer = request.user
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=customer)
    order_line, created = OrderLine.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_line.quantity = (order_line.quantity + 1)
    elif action == 'remove':
        order_line.quantity = (order_line.quantity - 1)
    order_line.save()
    if order_line.quantity <= 0:
        order_line.delete()
    return JsonResponse('Item was added', safe=False)
