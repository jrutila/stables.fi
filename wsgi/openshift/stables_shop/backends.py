from django.utils.translation import ugettext_lazy as _
from shop.shipping.backends.flat_rate import FlatRateShipping
from django.conf.urls import patterns, url
from django.db import models
from shop.models import Product, OrderItem, Order

class ProductActivator(models.Model):
    INITIATED = 10
    ACTIVATED = 20
    FAILED = 30
    CANCELED = 40

    STATUS_CODES = (
            (INITIATED, _('Initiated')),
            (ACTIVATED, _('Activated')),
            (FAILED, _('Failed')),
            (CANCELED, _('Canceled')),
            )
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order, related_name="activators")
    order_item = models.ForeignKey(OrderItem)
    status = models.IntegerField(choices=STATUS_CODES, default=INITIATED)

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

    def ship(self, order):
        for oi in order.items.all():
            product = oi.product
            activator = product.get_activator()
            activator.product = product
            activator.order_item = oi
            activator.order = order
            activator.save()
            activator.activate()

def is_shipped(self):
    act_count = self.activators.count()
    return act_count > 0 and self.activators.filter(status=ProductActivator.ACTIVATED).count() == act_count

Order.is_shipped = is_shipped
