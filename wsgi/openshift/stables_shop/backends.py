from django.utils.translation import ugettext_lazy as _
from shop.shipping.backends.flat_rate import FlatRateShipping
from django.conf.urls import patterns, url

class DigitalShipping(FlatRateShipping):
    backend_name = 'digital'
    verbose_name = _('Digital')
    url_namespace = 'digital'

    def __init__(self, shop):
        self.shop = shop
        self.rate = 0

    def redirect(self, request):
        return self.shop.finished(self.shop.get_order(request))

    def get_urls(self):
        urlpatterns = patterns('',
                url(r'^$', self.redirect, name='digital'),
        )
        return urlpatterns
