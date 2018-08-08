from django.conf.urls import url
from menu.views import MenuView

urlpatterns = [
    url(r'^$', MenuView.as_view(), name='menu_page'),
]

