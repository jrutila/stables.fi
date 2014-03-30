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
from stables.models import Course
import datetime

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

class EnrollProduct(Product):
    course = models.ForeignKey(Course)
    automatic_disable = models.BooleanField()

    class Meta:
        pass

    def get_activator(self):
        return EnrollProductActivator()

def check_active(sender, instance, created, **kwargs):
    if instance.course.is_full():
        EnrollProduct.objects.filter(course=instance.course).update(active=False)
    elif instance.course.get_occurrences()[0].start < datetime.datetime.now():
        EnrollProduct.objects.filter(course=instance.course).update(active=False)
    else:
        EnrollProduct.objects.filter(course=instance.course).update(active=True)

from django.db.models.signals import post_save
from stables.models import Enroll
post_save.connect(check_active, sender=Enroll)

class EnrollProductActivator(ProductActivator):
    rider = models.ForeignKey(RiderInfo, null=True, blank=True)

    def activate(self):
        user = UserProfile.objects.find(self.order.shipping_address_text)

        if user:
            self.rider = user.rider
            self.product.course.enroll(user)
            self.status = self.ACTIVATED
            self.save()
