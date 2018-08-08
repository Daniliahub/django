# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Base, Slugged


class User(AbstractUser, Base):
    """
    user model
    """
    pass


class Address(Base, Slugged):
    """
    Address object, not used anywhere for now, but for future.
    if I get time, will implement.
    """
    address = models.TextField()
    phone_number = models.PositiveIntegerField()
    user = models.ForeignKey(User)

