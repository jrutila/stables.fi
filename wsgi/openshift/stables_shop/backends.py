from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from shop.shipping.backends.flat_rate import FlatRateShipping
from django.conf.urls import patterns, url
from django.db import models
from shop.models import Product, OrderItem, Order, Cart
from shop.util.decorators import order_required, on_method
from datetime import date
import paytrail
from django.core.urlresolvers import reverse

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

class PayTrailBackend(object):
    url_namespace='paytrail-payment'
    backend_name = _('Paytrail payment')
    template = 'shop/paytrail-payment-notify.html'

    def __init__(self, shop):
        self.shop = shop

    def get_urls(self):
        urlpatterns = patterns('',
                url(r'^$', self.paytrail_payment_view, name='paytrail-payment'),
                url(r'^success$', self.paytrail_payment_success, name='paytrail-success'),
                url(r'^notify$', self.paytrail_payment_notify, name='paytrail-notify'),
                url(r'^failure$', self.paytrail_payment_failure, name='paytrail-failure'),
                               )
        return urlpatterns

    @on_method(order_required)
    def paytrail_payment_view(self, request):
        order = self.shop.get_order(request)
        amount = self.shop.get_order_total(order)
        transaction_id = date.today().strftime('%Y') + '%06d' % order.id
        urls = {
            'success': request.build_absolute_uri(reverse('paytrail-success')),
            'notification': request.build_absolute_uri(reverse('paytrail-notify')),
            'failure': request.build_absolute_uri(reverse('paytrail-failure')),
            'pending': ''
                }
        redirect_url = paytrail.createPayment(order, amount, order.id, urls)
        order.status = Order.CONFIRMING
        order.save()
        return redirect(redirect_url)

    def _check_authcode(self, request):
        order_number = request.GET.get('ORDER_NUMBER')
        timestamp = request.GET.get('TIMESTAMP')
        paid = request.GET.get('PAID')
        method = request.GET.get('METHOD')
        authCode = paytrail.calcAuthCode(order_number, timestamp, paid, method)
        if authCode != request.GET.get('RETURN_AUTHCODE').lower():
            raise Exception("Authcode mismatch!")
        return order_number

    def paytrail_payment_success(self, request):
        order_number = self._check_authcode(request)
        order = Order.objects.get(pk=order_number)
        order.status = Order.CONFIRMED
        order.save()

    def paytrail_payment_failure(self, request):
        pass

    def paytrail_payment_notify(self, request):
        method = request.GET.get('METHOD')
        from shop.payment import api
        order_number = self._check_authcode(request)
        order = Order.objects.get(pk=order_number)
        api.PaymentAPI().confirm_payment(order, order.order_total, order.id, method)
