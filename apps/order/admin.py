# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from order.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    search_fields = ('title', 'status')

admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ('item__title', )

admin.site.register(OrderItem, OrderItemAdmin)

