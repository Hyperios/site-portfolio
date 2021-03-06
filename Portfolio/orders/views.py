from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import OrderCreated


def OrderCreate(request):
    cart = Cart(request)
    if cart.get_total_item() > 0:
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                cart.clear()
                OrderCreated(order.id) # Asynchronous message sending
                return render(request, 'orders/created.html', {'cart': cart, 'form': form, 'order': order})

        form = OrderCreateForm()
        return render(request, 'orders/create.html', {'cart': cart, 'form': form})
    else:
        return render(request, 'cart/detail.html', {'error_message': 'В вашей корзине нет товаров, сначала выберете товары'})


