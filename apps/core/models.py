# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from core.managers import BaseManager


class Base(models.Model):
    """
    Base model for all the models. All models should inherit from this model
    This models features created_at, updated_at, deleted objects
    """
    class Meta:
        abstract = True

    # Manager to handle deletes, nothing gets deleted from DB, they are just now shown to end user
    # Read more on core.managers file
    objects = BaseManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)


class Slugged(models.Model):
    """
    Abstract core model for titled models. Any model which has title should inherit this model
    """
    class Meta:
        abstract = True

    title = models.CharField(_('Title'), max_length=256)
    slug = models.CharField(_('Unique Identifier'), unique=True, max_length=256, blank=True)

    def __unicode__(self):
        return self.title

    def _get_slug(self):
        """
        Unique slug for objects
        """
        slug = ''
        if self.title:
            slug = '-'.join([slugify(self.title), unicode(uuid.uuid4())[:7]])
        return slug[:256]

    def save(self, *args, **kwargs):
        """
        on save populate slug from title else use uuid
        """
        self.slug = self._get_slug()
        return super(Slugged, self).save(*args, **kwargs)

