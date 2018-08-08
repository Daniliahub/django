# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models

from core.models import Base, Slugged
from menu.models import Item, Condiment, Variant, Size
from profiles.models import User


class Order(Base):
    """
    Model for orders. One order can have multiple items, to identify that which different items
    point to same order this model is important. This model also keeps track of order status and
    total order price
    """
    order_status = (
        ('ONGOING', 'Ongoing'),
        ('PLACED', 'Placed'),
        ('CONFIRMED', 'Confirmed'),
        ('OUTFORDELIVERY', 'Out For Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    total_price = models.FloatField()
    status = models.CharField(choices=order_status, default='PLACED', max_length=20)


class OrderItem(Base):
    """
    OrderItem model is for each item placed in a single order. This will have details of which
    variant and which condiments has been added to the item.
    """
    order = models.ForeignKey(Order)
    item = models.ForeignKey(Item)
    size = models.ForeignKey(Size)
    condiments = models.ManyToManyField(Condiment, blank=True)
    variant = models.ForeignKey(Variant, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
