from shop.models import Product
from django.db import models
from stables.models import TicketType
from durationfield.db.models.fields.duration import DurationField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from stables_shop.backends import ProductActivator
from stables.models import UserProfile
from stables.models import Ticket
from stables.models import RiderInfo

class DigitalShippingAddressModel(models.Model):
    name = models.TextField()

    def as_text(self):
        return self.name

class TicketProduct(Product):
    ticket = models.ForeignKey(TicketType)
    amount = models.PositiveIntegerField(default=1)
    duration = DurationField(blank=True, null=True)
    expires = models.DateField(blank=True, null=True)

    class Meta:
        pass

    def clean(self):
        if not(self.duration or self.expires):
            raise ValidationError(_("Ticket duration or absolute expire date must be set"))

    def get_activator(self):
        return TicketProductActivator()

class TicketProductActivator(ProductActivator):
    start = models.PositiveIntegerField(null=True)
    end = models.PositiveIntegerField(null=True)
    rider = models.ForeignKey(RiderInfo, null=True, blank=True)
    duration = DurationField(blank=True, null=True)

    def activate(self):
        user = UserProfile.objects.find(self.order.shipping_address_text)
        if user:
            self.rider = user.rider
            for i in range(0, self.product.amount):
                t = Ticket.objects.create(
                        type=self.product.ticket,
                        owner=self.rider)
                if i == 0: self.start = t.id
                if i == self.product.amount-1: self.end = t.id
            self.duration = self.product.duration
            self.status = self.ACTIVATED
            self.save()
