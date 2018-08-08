# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

from menu.models import Item


class MenuView(TemplateView):
    """
    View to show menu
    """
    template_name = "menu/menu.html"

    def get_context_data(self, **kwargs):
        context = super(MenuView, self).get_context_data(**kwargs)
        message_code = self.request.GET.get('message-code')
        groups = {}
        context = {
            'groups': groups,
            'message_code': message_code,
        }
        items = Item.objects.prefetch_related(
            'allowed_condiments', 'allowed_variants'
        ).select_related('group').all()

        for item in items:
            if item.group not in groups:
                groups[item.group] = []
            groups[item.group].append(item)
        return context

