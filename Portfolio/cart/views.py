from django.shortcuts import render
from django.views.decorators.http import require_POST
from shop.models import PhotoTech
from .cart import Cart
from .forms import CartAddProductForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

def update_cart_args(request):
    """This method get args to all template responce view"""
    cart = Cart(request)
    context = {}
    context['cart_total_item'] = cart.get_total_item()
    context['cart_total_price'] = cart.get_total_price()
    return context

@csrf_protect
def add_product_front(request):
    update_quantity = False
    cart = Cart(request)
    price = request.POST.get('price', None)
    ids = request.POST.get('id', None)
    product_id = str(ids)
    if product_id not in cart.session['cart']:
        cart.session['cart'][product_id] = {'quantity': 0,
                                 'price': str(price)}

    if update_quantity:
        cart.session['cart'][product_id]['quantity'] = 1
    else:
        cart.session['cart'][product_id]['quantity'] += 1
    cart.session.save()

    data = { 
            'count' : cart.get_total_item(), 
            'total_price' : cart.get_total_price()}
    return JsonResponse(data)


@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(PhotoTech, product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    return redirect('cart:CartDetail')


def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(PhotoTech, ids=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')

def CartDetail(request):
    cart = Cart(request)
    args = {'cart': cart}
    args.update(update_cart_args(request))
    return render(request, 'cart/detail.html', args)

@require_POST
def add_one_or_remove(request):
	cart = Cart(request)
	ids = request.POST.get('ids', None)
	col = request.POST.get('col', None)
	cart.remove_add(ids, col)
	count = cart.session['cart'][ids]['quantity']
	total_id_price = cart.get_total_item_price(ids)
	data = {'col' : count,
	        'ids' : '#opt%s' % ids,
	        'total_item_price' : total_id_price,
	        'total_item_id' : '#total_price%s' % ids}
	data.update(update_cart_args(request))
	return JsonResponse(data)

def remove_all(request):
	cart = Cart(request)
	cart.clear()
	data = {}
	data.update(update_cart_args(request))
	return JsonResponse(data)

