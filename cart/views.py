from .cart import Cart
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from catalog.models import RADIATOR_CLASSES
import json


@csrf_exempt
def add_product_view(request):
    post_data = request.POST
    if request.method == 'POST':
        cart = Cart(request)
        id = post_data.get('id')
        type = post_data.get('type')
        cart.add(id, type)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def remove_product_view(request):
    post_data = request.POST
    if request.method == 'POST':
        cart = Cart(request)
        id = post_data.get('id')
        cart.remove(id)
        args = {'items': cart.items, 'total_price': cart.total_price}
        return render(request, 'cart/cart.html', args)

@csrf_exempt
def cart_view(request):
    cart = Cart(request)
    args = {'items': cart.items, 'total_price': cart.total_price}
    return render(request, 'cart/cart.html', args)

@csrf_exempt
def change_quantity_view(request):
    post_data = request.POST
    if request.method == 'POST':
        cart = Cart(request)
        id = post_data.get('id')
        if post_data.get('remove'):
            cart.update_quantity(id, -1)
        if post_data.get('add'):
            cart.update_quantity(id, 1)
        args = {'items': cart.items, 'total_price': cart.total_price}
        return render(request, 'cart/cart.html', args)



