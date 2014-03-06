from django.conf.urls import patterns, url
from views import HomePageView, PayView, ShipView
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view()),
    url(r'^paid/', PayView.as_view(), name='order-paid'),
    url(r'^ship/', ShipView.as_view(), name='order-ship'),
)

