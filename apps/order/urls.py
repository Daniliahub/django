from django.conf.urls import url
from order.views import (
    AllOrdersView, GroupByType, GroupBySize,
    AddToCartView)


urlpatterns = [
    # url(r'^order/$', OrderView.as_view()),
    url(r'^orders/$', AllOrdersView.as_view(), name='all_orders'),
    url(r'^orders-by-type/$', GroupByType.as_view()),
    url(r'^orders-by-size/$', GroupBySize.as_view()),
    url(r'^add-to-cart/(?P<item_id>(\d+))$', AddToCartView.as_view(), name='add_to_cart'),
]

