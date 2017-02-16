# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import PhotoTech
from orders.models import Order, OrderItem

class PhotoTechInline(admin.TabularInline):
    model = PhotoTech
    extra = 6


class PhotoTechAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                    {'fields': ['name_model']}),
        ('Дата',                  {'fields': ['pub_date']}),
        ('Картинка',              {'fields': ['image_url']}),
        ('Наличие',               {'fields': ['available']}),
        ('Цена',                  {'fields': ['price']}),
        ('Описание',              {'fields': ['text_prev']}),
        ('Разрешение матрицы',    {'fields': ['matrix_resol']}),
        ('Размер матрицы',        {'fields': ['matrix_size']}),
        ('Масимальное разрешение',{'fields': ['max_resol']}),
        ('Зум',                   {'fields': ['zoom']}),
        ('Цвет',                  {'fields': ['color']}),
        ('Страна производитель',  {'fields': ['country']}),

    ]
    list_display = ('ids', 'name_model', 'pub_date', 'image_url', 'available', 
    	            'text_prev', 'matrix_resol', 'matrix_size', 'max_resol',
    	            'zoom', 'color', 'country')
    list_filter = ['pub_date']
    search_fields = ['name_model']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(PhotoTech, PhotoTechAdmin)

admin.site.register(Order, OrderAdmin)