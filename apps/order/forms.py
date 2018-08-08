from django import forms

from menu.models import (
    Size, ItemGroup, SizedItemPrice, Variant, Condiment
)
from order.models import Order, OrderItem, Condiment
from profiles.models import User


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        all_sizes = Size.objects.values_list('title', flat=True)
        all_types = ItemGroup.objects.values_list('title', flat=True)
        for size in all_sizes:
            self.fields['size_{0}'.format(size)] = forms.BooleanField(label=size, required=False)
        for bev_type in all_types:
            self.fields['type_{0}'.format(bev_type)] = forms.BooleanField(label=bev_type, required=False)

    def _get_attr_name(self, name):
        return name.split('_')[1]

    def clean(self):
        data = super(FilterForm, self).clean()
        cleaned_data = {
            'size': [],
            'type': [],
        }
        for key, value in data.iteritems():
            if key.startswith('size') and value:
                attr_name = self._get_attr_name(key)
                cleaned_data['size'].append(attr_name)
            elif key.startswith('type') and value:
                attr_name = self._get_attr_name(key)
                cleaned_data['type'].append(attr_name)
        return cleaned_data


class AddToCartForm(forms.Form):
    """
    Form to add items to a cart via a modal.
    """

    size = forms.ChoiceField(choices=[], widget=forms.RadioSelect())
    variant = forms.ChoiceField(choices=[], widget=forms.RadioSelect(), required=False)
    condiments = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple(), required=False
    )

    def get_allowed_variant_choices(self):
        """
        Get allowed variant choices in the format:

        Returns:
            [(<variant_id_1, <variant_title_1>),
            (<variant_id_2, <variant_title_2>)]

        """
        variants = self.item.allowed_variants.all()
        return [
            (variant.id, u'{title} - ${price}'.format(
                title=variant.title, price=variant.price)) for variant in variants
        ]


    def get_allowed_condiment_choices(self):
        """
        Get allowed condiment choices in the format:

        Returns:
            [(<condiment_id_1, <condiment_title_1>),
            (<condiment_id_2, <condiment_title_2>)]
        """
        condiments = self.item.allowed_condiments.all()
        return [
            (condiment.id, u'{title} - ${price}'.format(
                title=condiment.title, price=condiment.price)) for condiment in condiments
        ]


    def get_allowed_size_choices(self):
        """
        Get allowed condiment choices in the format:

        Returns:
            [(<size_id_1, <size_title_1>),
            (<size_id_2, <size_title_2>)]

        """
        sized_item_prices = SizedItemPrice.objects.select_related(
            'size').filter(item=self.item)

        return [
            (sized_item_price.id, u'{title} - ${price}'.format(
                title=sized_item_price.size.title, price=sized_item_price.price))
            for sized_item_price in sized_item_prices
        ]


    def __init__(self, item, *args, **kwargs):
        super(AddToCartForm, self).__init__(*args, **kwargs)
        self.item = item

        self.fields['variant'].choices = self.get_allowed_variant_choices()
        self.fields['condiments'].choices = self.get_allowed_condiment_choices()
        self.fields['size'].choices = self.get_allowed_size_choices()

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        variant_id = data.get('variant')
        size_id = data.get('size')
        condiment_ids = data.get('condiments')

        user = User.objects.first()

        variant = None
        if variant_id:
            variant = Variant.objects.get_or_none(id=variant_id)
        sized_item_price = SizedItemPrice.objects.get(id=size_id)
        condiments = Condiment.objects.filter(id__in=condiment_ids)

        condiments_price = sum([condiment.price for condiment in condiments])
        total_price = sized_item_price.price + condiments_price
        if variant:
            total_price += variant.price

        order = Order.objects.create(
            user=user, status='PLACED', total_price=total_price)


        order_item = OrderItem.objects.create(
            order=order, item=sized_item_price.item, size=sized_item_price.size,
            variant=variant, quantity=1, total_price=total_price
        )
        order_item.condiments.add(*condiment_ids)
