#from shop.models import Product
from django.db import models
from stables.models import TicketType, Participation
from durationfield.db.models.fields.duration import DurationField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from stables_shop.backends import ProductActivator
from stables.models import UserProfile
from stables.models import Ticket
from stables.models import RiderInfo
from stables.models import Course
from django.utils import timezone
import datetime
from shop.models import Product
from django_settings.models import Model as SettingsModel
from django_settings.models import registry
from django.core.urlresolvers import reverse

class LongString(models.Model):
   value = models.TextField()

   class Meta:
       abstract = True
registry.register(LongString)

class DigitalShippingAddressModel(models.Model):
    name = models.TextField()

    def as_text(self):
        return self.name

def _getUserName(address):
    return address.split('\n')[0]

class TicketProduct(Product):
    ticket = models.ForeignKey(TicketType)
    amount = models.PositiveIntegerField(help_text=_("Amount of tickets included in this product."))
    duration = DurationField(blank=True, null=True, help_text=_("Relative duration of the given product. For example 30 days, 90 days. If this is empty, you must insert expire date."))
    expires = models.DateField(blank=True, null=True, help_text=_("Absolute expiration date for the given product. For example 2014-12-31. If this is empty, you must insert duration."))

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
        user = UserProfile.objects.find(_getUserName(self.order.shipping_address_text))
        if user:
            self.rider = user.rider
            for i in range(0, self.product.amount):
                exp = None
                if self.product.expires:
                    exp = self.product.expires
                t = Ticket.objects.create(
                        type=self.product.ticket,
                        owner=self.rider,
                        expires=exp)
                if i == 0: self.start = t.id
                if i == self.product.amount-1: self.end = t.id
            self.duration = self.product.duration
            self.status = self.ACTIVATED
            self.save()

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Ticket)
def ticket_expirer(sender, **kwargs):
    ticket = kwargs['instance']
    if ticket.transaction and not ticket.expires:
        actr = TicketProductActivator.objects.filter(start__lte=ticket.id, end__gte=ticket.id)
        if actr:
            actr = actr[0]
            exp = datetime.datetime.combine(
                    ticket.transaction.source.start.date()+actr.duration,
                    datetime.time(23,59,59))
            Ticket.objects.filter(id__gte=actr.start, id__lte=actr.end).update(expires=exp)

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
    elif instance.course.get_occurrences()[0].start < timezone.now():
        EnrollProduct.objects.filter(course=instance.course).update(active=False)
    else:
        EnrollProduct.objects.filter(course=instance.course).update(active=True)

from django.db.models.signals import post_save
from stables.models import Enroll
post_save.connect(check_active, sender=Enroll)

class EnrollProductActivator(ProductActivator):
    rider = models.ForeignKey(RiderInfo, null=True, blank=True)

    def activate(self):
        user = UserProfile.objects.find(_getUserName(self.order.shipping_address_text))

        if user:
            self.rider = user.rider
            self.product.course.enroll(user)
            self.status = self.ACTIVATED
            self.save()

def get_short_url_for(partid):
     shortUrl = PartShortUrl.objects.filter(participation=partid)
     if shortUrl.count() == 1:
         return reverse('shop-pay', kwargs={ 'hash': shortUrl[0].hash })
     return reverse('shop-pay', kwargs={ 'id': partid })

import string
from markov_passwords import MarkovChain, finnish
chain = MarkovChain(c for c in finnish.lower() if c in string.ascii_lowercase)

def generate_hash():
    import itertools
    hash = ''.join(itertools.islice(chain, 12))
    return hash

class PartShortUrl(models.Model):
    participation = models.ForeignKey(Participation, unique=True)
    hash = models.CharField(unique=True, max_length=12, default=generate_hash)

    def __unicode__(self):
        return "%s - %s" % (self.hash, self.participation)

