# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from menu.models import (Item, ItemGroup, Variant, Condiment,
                        Size, SizedItemPrice)


class ItemGroupAdmin(admin.ModelAdmin):
    search_fields = ('title', )

admin.site.register(ItemGroup, ItemGroupAdmin)


class ItemAdmin(admin.ModelAdmin):
    search_fields = ('title', 'group__title')

admin.site.register(Item, ItemAdmin)


class CondimentAdmin(admin.ModelAdmin):
    search_fields = ('title', 'group__title')

admin.site.register(Condiment, CondimentAdmin)


class SizeAdmin(admin.ModelAdmin):
    search_fields = ('title', )

admin.site.register(Size, SizeAdmin)


class VariantAdmin(admin.ModelAdmin):
    search_fields = ('title', 'group__title')

admin.site.register(Variant, VariantAdmin)


class SizedItemPriceAdmin(admin.ModelAdmin):
    search_fields = ('item__title', 'item__group__title', 'size__title')

admin.site.register(SizedItemPrice, SizedItemPriceAdmin)
