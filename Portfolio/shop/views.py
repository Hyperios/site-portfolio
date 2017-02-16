# -*- coding: utf-8 -*-

from django.views.generic import *
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_protect, \
                                         ensure_csrf_cookie, \
                                         requires_csrf_token

from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.views import password_reset, \
                                      password_reset_confirm, \
                                      password_reset_done
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages, auth
from django.template.response import TemplateResponse
from django.utils import encoding

from django.utils import timezone

from django.template.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect 
from django.http import HttpResponse, HttpResponseServerError
from django.http import HttpResponseNotFound
from django.template import RequestContext

from django import forms
from .forms import RegistrationForm, MyPasswordRestartForm
from .models import UserProfile
from cart.cart import Cart
import hashlib, datetime, random

from .models import PhotoTech
import json

def update_cart_args(request):
    """This method get args to all template responce view"""
    cart = Cart(request)
    context = {}
    context['cart_total_item'] = cart.get_total_item()
    context['cart_total_price'] = cart.get_total_price()
    return context

class ShopView(ListView):
    model = PhotoTech
    template_name = 'shop/index.html'
    
    def get_queryset(self):
        return PhotoTech.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        context.update(update_cart_args(self.request))
        return context

    
class PhotoView(ListView):
    model = PhotoTech
    template_name = 'shop/photo.html'
    context_object_name = 'latest_photo_list'
    queryset  = PhotoTech.objects.filter(pub_date__lte=timezone.now())
    count_product  = '25'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        context.update(update_cart_args(self.request))
        context.update({ 'filter_fields': PhotoView._all_fields_all_data()})
        return context

    def _all_data_fields(field):
        """If no item in form list, then all item"""
        all_fields = PhotoTech.objects.all().values()
        return list(set([all_fields[x][field]
                    for x in range(len(all_fields))]))

    def _all_fields_all_data():
        """Return all data in all fields for template filter in a dict.
        When someone will added new kinde of value in product field,
        this value displayed in filtering fields"""
        all_fields = PhotoTech.objects.all().values()[0].keys()
        all_data = [PhotoView._all_data_fields(x) for x in all_fields]
        allowed_search_fields = ['zoom',
                                 'matrix_resol',
                                 'color',
                                 'matrix_size',
                                 'country']
        return {x: y for x, y in zip(all_fields, all_data)
                if x in allowed_search_fields}

    def _get_object_page_filter(self, request, filter_dict, page=1):
        sets = PhotoTech.objects.filter(
            pub_date__lte=timezone.now()).filter(
            zoom__in=filter_dict['zoom']).filter(
            matrix_resol__in=filter_dict['matrix_resol']).filter(
            color__in=filter_dict['color']).filter(
            matrix_size__in=filter_dict['matrix_size']).filter(
            country__in=filter_dict['country'])

        paginator = Paginator(sets, int(filter_dict['paginate_b']))
        page_obj = paginator.page(page)
        sets = page_obj.object_list

        args = {'latest_photo_list': sets,
                'is_paginated': True,
                'page_obj': page_obj,
                'paginator': paginator,
                'filter_dict': filter_dict
                }
        args.update(update_cart_args(request))
        args.update({ 'filter_fields': PhotoView._all_fields_all_data()})
        return render(request, PhotoView.template_name, args)
    

    def post(self, request, *args, **kwargs):
        """For POST request, take filtered data and get
        in template"""
        paginate_b = request.POST.get('pages_elements', None)
        filter_dict = { 'paginate_b': paginate_b }

        # If request haven data in fields, then taked all data
        allowed_fields = ['zoom',
                          'matrix_resol',
                          'color',
                          'matrix_size',
                          'country']
        for x, y in [(x, request.POST.getlist(x)) for x in allowed_fields]:
            if y != []:
                filter_dict[x] = y
            else: 
                filter_dict[x] = PhotoView._all_data_fields(x)

        return PhotoView._get_object_page_filter(self, request, filter_dict)

        
    def paginate_next(request):
        filter_dict = request.POST.get('filter_dict')
        page = int(request.POST.get('page'))

        # Try to get data 0 if request method GET, and > 0 if POST
        if len(filter_dict) == 0:
            filter_dict = {
                       'paginate_b' : PhotoView.paginate_by
                    }
            filter_dict.update(PhotoView._all_fields_all_data())
        else:
            """JSON format it is data whith "" but, it take '',
            this function fix it"""
            filters = ""
            for x in filter_dict:
                if x == "'":
                    x = '"'
                    filters += x
                else:
                    filters += x

            filter_dict = ''.join([x for x in filter_dict if x != '+'])
            filter_dict = json.loads(filters)

        return PhotoView._get_object_page_filter(request, 
                                                 request, 
                                                 filter_dict, 
                                                 page)

    def register_success(request):
        """Redirect for success registration"""
        return render(request, 'shop/register_success.html')

    def login_view(request):
        """Check post request for login form in general view"""
        username2 = request.POST.get('username', None)
        username = request.POST['username']
        password = request.POST['password']
        print(username, password, username2)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active == True:
            login(request, user)
            return HttpResponseRedirect("/shop/photo/")
        else:
            messages.add_message(request,
                                 messages.INFO,
                                'ÐÐµÐ²ÐµÑ€Ð½Ñ‹Ð¹ Ð»Ð¾Ð³Ð¸Ð½ Ð¸Ð»Ð¸ \
                                 Ð¿Ð°Ñ€Ð¾Ð»ÑŒ')
            return HttpResponseRedirect("/shop/photo/")



class DetailPhotoView(DetailView):
    model = PhotoTech
    template_name = 'shop/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailPhotoView, self).get_context_data(**kwargs)
        context.update(update_cart_args(self.request))
        return context

    def get_queryset(self):
        return PhotoTech.objects.filter(pub_date__lte=timezone.now())


@csrf_protect
def results(request):
    if request.method == 'POST':
        def get_context_data(self, **kwargs):
            context = super(SearchView, self).get_context_data(**kwargs)
            context['color'] = request.POST['color']
            context.update(update_cart_args(request))
            return context
    else: 
        pass
    return render(request, 'shop/photo.html')


# user registration and confirm from email
def register_user(request):
    """View method for registration form,
    send mail whith confirmation link"""
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        args.update(update_cart_args(request))
        if form.is_valid():
            form.save() # save user to database if form is valid
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1((str(random.random())).encode('utf-8')
                                                     ).hexdigest()[:5]
            activation_key = hashlib.sha1(salt.encode('utf-8') +
                             email.encode('utf-8')).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user,
                                      activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'ÐŸÐ¾Ð´Ñ‚Ð²ÐµÑ€Ð¶Ð´ÐµÐ½Ð¸Ðµ \
                             Ñ€ÐµÐ³Ð¸ÑÑ‚Ñ€Ð°Ñ†Ð¸Ð¸'
            email_body = "Приветствуем %s, спасибо что подписались. \
            Для активации вашего аккаунта перейдите по этой ссылке в течении \
            48 часов: http://139.162.240.128/shop/confirm/%s" \
            % (username, activation_key)

            send_mail(email_subject,
                    email_body,
                    'admin@example.com', 
                    [email], 
                    fail_silently=False)
            return HttpResponseRedirect('/shop/register_success')
    else:
        args['form'] = RegistrationForm()
        args.update(update_cart_args(request))
    return render(request, 'shop/register.html', args)


def register_confirm(request, activation_key):
    # check if user is already logged in and 
    # if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/shop/')

    # check if there is UserProfile which matches 
    # the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, 
                                     activation_key=activation_key)

    # check if the activation key has expired, 
    # if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('shop/confirm_expired.html')
    #if the key hasn't expired save user and set him
    # as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    args = {}
    args.update(update_cart_args(request))
    return render(request, 'shop/register_confirm.html', args)


@csrf_protect
def password_reload(request):
    args = {}
    args.update(csrf(request))
    args.update(update_cart_args(request))
    if request.method == 'POST':
        form = MyPasswordRestartForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save(request)     
            return HttpResponseRedirect('/shop/password_reset/done/')
    else:
        args['form'] = PasswordResetForm()

    return render(request, 'shop/password_restart.html', args)


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, 
                              template_name='shop/reset_confirm.html',
                              uidb64=uidb64, 
                              token=token, 
                              post_reset_redirect = '../../../../reset/done/')


def success(request):
    args = {}
    args.update(update_cart_args(request))
    return render_to_response("shop/success.html", args)    


def success_reset(request):
    args = {}
    args.update(update_cart_args(request))
    return render_to_response("shop/success_reset.html", args) 


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/shop/")


def error_404(request):
    return HttpResponseNotFound("""<h2 style="text-align:center;">404</h2> 
                                 <div style="text-align:center;"><a  
                                 href="http://139.162.240.128/shop/"> 
                                 Перейти на главную</a><div>""")

def error_500(request):
    return HttpResponseServerError("""<h2 style="text-align:center;">404</h2> 
                                 <div style="text-align:center;"><a  
                                 href="http://139.162.240.128/shop/"> 
                                 Перейти на главную</a><div>""")
