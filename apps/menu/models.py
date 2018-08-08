# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.validators import MinValueValidator
from django.db import models

from core.models import Base, Slugged


class ItemGroup(Base, Slugged):
    """
    Order type model i.e tea and coffee
    """
    pass


class Condiment(Base, Slugged):
    """
    Condiments model i.e any condiments which can be optionally added to order types (coffee, tea etc.)
    Multiple or none condiments can be added to an order
    """
    price = models.FloatField()
    group = models.ForeignKey(ItemGroup)

    class Meta:
        unique_together = ('title', 'group')

    def __unicode__(self):
        return ' - '.join([self.group.title, self.title])


class Variant(Base, Slugged):
    """
    Variant model i.e any variant which can be optionally added to an order
    only one or none variant can be addedd to an order
    """
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    group = models.ForeignKey(ItemGroup)

    class Meta:
        unique_together = ('title', 'group')

    def __unicode__(self):
        return ' - '.join([self.group.title, self.title])


class Item(Base, Slugged):
    """
    Item model
    """
    group = models.ForeignKey(ItemGroup)
    allowed_condiments = models.ManyToManyField(Condiment, blank=True)
    allowed_variants = models.ManyToManyField(Variant, blank=True)

    def __unicode__(self, *args, **kwargs):
        return u'{item} - {group}'.format(item=self.title, group=self.group.title)

    def base_price(self):
        """
        base price of an item, minimum price available for an item (small sized coffee)
        """
        return min(self.sizeditemprice_set.values_list('price', flat=True))

    def get_sized_item_prices(self):
        """
        An item will have multiple size and multiple size will have multiple price, this is
        to show
        """
        data = []
        for item_size in self.sizeditemprice_set.all():
            data.append({
                'id': item_size.id,
                'size': item_size.size.title,
                'price': item_size.price,
            })

        return json.dumps(data)

    def get_allowed_condiments(self):
        """
        One type of item (coffee or tea) can have multiple condiments, but all condiments
        are not allowed for all items
        """
        data = []
        for condiment in self.allowed_condiments.all():
            data.append({
                'id': condiment.id,
                'title': condiment.title,
                'price': condiment.price,
            })

        return json.dumps(data)

    def get_allowed_variants(self):
        """
        One type of item (coffee or tea) can have a variant (hot or cold)
        """
        data = []
        for variant in self.allowed_variants.all():
            data.append({
                'id': variant.id,
                'title': variant.title,
                'price': variant.price,
            })

        return json.dumps(data)


class Size(Base, Slugged):
    """
    Size of items
    """
    pass


class SizedItemPrice(Base):
    """
    Price model for each size
    """
    item = models.ForeignKey(Item)
    size = models.ForeignKey(Size)
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        unique_together = ('item', 'size')

    def __unicode__(self):
        return ' - '.join([self.size.title, self.item.title])

