# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View, TemplateView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from order.forms import FilterForm, AddToCartForm
from order.models import Order, OrderItem
from menu.models import ItemGroup, Size, Item


class AllOrdersView(View):
    """
    View to show all the past orders.
    This view also features a filter i.e. if you want to see all the coffee orders which are of tall and venti size.
    """
    template_name = "order/all_orders.html"

    def get(self, request, *args, **kwargs):
        """
        Will show all orders placed till date and total sales and also renders a form to filter by type and/or size.
        """
        context = {}
        context['form'] = FilterForm()
        all_orders = list(OrderItem.objects.all().order_by('-updated_at'))
        context['all_orders'] = all_orders
        context['total_sales'] = sum([_.total_price for _ in all_orders])
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Filteration view. If user wants to filter all tall coffee orders or all tall and venti tea orders this View
        makes that happen.
        """
        form = FilterForm(request.POST)
        context = {}
        context['form'] = form
        if form.is_valid():
            data = form.cleaned_data
            args = []
            # if user tries to filter by types and sizes both, we should select the orders which are of the same types
            # (multiple types and sizes are supported)
            if data['type'] and data['size']:
                all_orders = OrderItem.objects.select_related('size', 'item', 'item__group').filter(
                    Q(item__group__title__in=data['type']) & Q(size__title__in=data['size'])).order_by('-updated_at')
            # If user wants to filter by only types (multiple type supported)
            elif data['type']:
                all_orders = OrderItem.objects.select_related('size', 'item', 'item__group').filter(
                    Q(item__group__title__in=data['type'])).order_by('-updated_at')
            # If user wants to filter by only sizes (multiple size supported)
            elif data['size']:
                all_orders = OrderItem.objects.select_related('size', 'item', 'item__group').filter(
                    Q(size__title__in=data['size'])).order_by('-updated_at')
            # If user doesn't select anything, either we should show nothing or we should show everything, I'm showing
            # all the orders
            else:
                all_orders = OrderItem.objects.all().order_by('-updated_at')
            context['all_orders'] = all_orders
            context['total_sales'] = sum([_.total_price for _ in all_orders])
            return render(request, self.template_name, context)
        # If the form is invalid (which is a rare scenario)
        else:
            return HttpResponse('Bad request!')


class GroupedOrder(TemplateView):
    """
    Parent view for grouping orders by type or size, in future if we want to add different way of grouping this will help user
    achieving the same without duplicating any code, see the views `GroupByType` and `GroupBySize` views.
    """
    template_name = 'order/group_by.html'

    @staticmethod
    def _get_group_name(*args):
        """
        This function must be implemented by child classes
        """
        raise NotImplementedError

    def get_context_data(self):
        context = super(GroupedOrder, self).get_context_data()
        all_orders = OrderItem.objects.select_related('item', 'item__group', 'size').filter().order_by('-updated_at')
        orders = {}
        grouped_sales = {}
        total_sales = 0
        for order in all_orders:
            group_name = self._get_group_name(order)
            if group_name not in orders:
                orders[group_name] = []
                grouped_sales[group_name] = 0
            orders[group_name].append(order)
            total_sales += order.total_price
            grouped_sales[group_name] += order.total_price

        context['orders'] = orders
        context['grouped_sales'] = grouped_sales
        context['total_sales'] = total_sales
        return context


class GroupByType(GroupedOrder):

    @staticmethod
    def _get_group_name(order):
        """
        Filter by order type i.e. coffee or tea
        """
        return order.item.group.title


class GroupBySize(GroupedOrder):

    @staticmethod
    def _get_group_name(order):
        """
        Filer by order size i.e tall, venti etc.
        """
        return order.size.title


class AddToCartView(View):
    template_name = "order/add_to_cart.html"

    def get(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        add_to_cart_form = AddToCartForm(item)
        context = {
            'add_to_cart_form': add_to_cart_form,
            'show_variants': add_to_cart_form.fields['variant'].choices,
            'show_condiments': add_to_cart_form.fields['condiments'].choices,
        }

        return render(request, self.template_name, context)

    def post(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        add_to_cart_form = AddToCartForm(item, request.POST)

        if add_to_cart_form.is_valid():
            add_to_cart_form.save()
        menu_page = reverse('menu_page')
        menu_page = '{menu_page_url}?message-code={message}'.format(
            menu_page_url=menu_page,
            message='orderPlaced'
        )
        return redirect(menu_page)
