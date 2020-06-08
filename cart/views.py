from .cart import Cart
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from .forms import OrderForm
from catalog.models import RADIATOR_CLASSES
import json


@csrf_exempt
def add_product_view(request):
    post_data = request.POST
    if request.method == 'POST':
        cart = Cart(request)
        id = post_data.get('id')
        type = post_data.get('type')
        more = ''
        if post_data.get('color'):
            more = post_data.get('color')
        cart.add(id, type, more)
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


@csrf_exempt
def checkout_view(request):
    cart = Cart(request)
    if not cart.items:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    form = OrderForm()
    return render(request, 'cart/checkout.html', {'form': form})


@csrf_exempt
def send_mail_view(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            message = f'Клиент: {form.cleaned_data["name"]}\n' \
                      f'Номер телефона: {form.cleaned_data["phone_number"]}\n' \
                      f'Удобное время: {form.cleaned_data["more_info"]}\n' \
                      f'Заказы:\n'
            for key, value in cart.items.items():
                message += f'{value["options"]}\n' \
                           f'Заказанное количество: {value["quantity"]}\n\n'

            html_message = f'<b>Клиент:</b> {form.cleaned_data["name"]}<br>' \
                      f'<b>Номер телефона:</b> {form.cleaned_data["phone_number"]}<br>' \
                      f'<b>Удобное время:</b> {form.cleaned_data["more_info"]}<br>' \
                      f'<b>Заказы:</b><br><br><pre>'
            for key, value in cart.items.items():
                html_message += f'{value["options"]}<br>' \
                           f'<b>Заказанное количество:</b> {value["quantity"]}<br><br>'
            html_message += '</pre>'

            # send_mail('Новый заказ', message, 'behumbleplez@gmail.com',
            #           ['valentin.kolesnikov.work@gmail.com'], fail_silently=False)

            subject, from_email, to = 'Новый заказ', 'behumbleplez@gmail.com', 'valentin.kolesnikov.work@gmail.com'
            msg = EmailMultiAlternatives(subject, message, from_email, [to])
            msg.attach_alternative(html_message, "text/html")
            msg.send()

    return redirect('main_page_view')