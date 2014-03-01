from shop.models import Product
from django.db import models

class TicketProduct(Product):
    class Meta:
        pass

class DigitalShippingAddressModel(models.Model):
    name = models.TextField()

    def as_text(self):
        return self.name
