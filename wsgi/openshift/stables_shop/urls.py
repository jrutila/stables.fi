from django.conf.urls import patterns, url
from views import HomePageView, PayView, ShipView
from views import EditProduct, CreateProduct
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view()),
    url(r'^paid/', PayView.as_view(), name='order-paid'),
    url(r'^ship/', ShipView.as_view(), name='order-ship'),
    url(r'^product/(?P<pk>\d+)/edit/', EditProduct.as_view(), name='product-edit'),
    url(r'^product/add/(?P<content_type_id>\d+)', CreateProduct.as_view(), name='product-add'),
)

