from decimal import Decimal
from django.conf import settings
from shop.models import PhotoTech


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = PhotoTech.objects.filter(ids__in=product_ids)
        for product in products:
            self.cart[str(product.ids)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Количество товаров
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.ids)
        available = PhotoTech.objects.filter(ids=product_ids).values()[0]['available']
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity: # Для функционала если указывается количество добавляемых товаров
            self.cart[product_id]['quantity'] = quantity
        else:
            if quantity + 1 <= available: # Не будет добавлять сверх наличия
                self.cart[product_id]['quantity'] += quantity
            else:
                pass
        self.save()

    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.ids)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_item_price(self, item_ids):
        return int(self.cart[item_ids]['price']) * int(self.cart[item_ids]['quantity'])

    def get_total_item(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    def remove_add(self, product_ids, readd):
        available = PhotoTech.objects.filter(ids=product_ids).values()[0]['available']

        if (readd == "+1") and (self.cart[product_ids]['quantity'] < available):
            self.cart[product_ids]['quantity'] += 1

        if (readd == "-1") and (0 < self.cart[product_ids]['quantity']):
            self.cart[product_ids]['quantity'] -= 1
        self.save()



