from decimal import Decimal
from django.conf import settings
from catalog.models import RADIATOR_CLASSES


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.items = cart

        if cart:
            self.total_price = self.get_total_price()
        else:
            self.total_price = 0

    def update_quantity(self, id, quantity=1):
        self.items[id]['quantity'] += quantity
        if self.items[id]['quantity'] < 1:
            self.items[id]['quantity'] = 1
        self.save()

    def add(self, id, type):
        cart_id = f'{type}{id}'
        item_class = RADIATOR_CLASSES[type]
        item = item_class.objects.get(id=id)

        if cart_id not in self.items:
            self.items[cart_id] = {
                'name': item.__str__(),
                'image': item.photo.url,
                'price': item.price,
                'quantity': 1,
                'description': item.description,
                'options': item.get_description()
            }
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.items
        self.session.modified = True
        self.total_price = self.get_total_price()

    def remove(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        price = 0
        for key, value in self.items.items():
            price += int(self.items[key]['quantity']) * Decimal(self.items[key]['price'])
        return price
