from django.db import models
from shop.models_bases import BaseProduct

class Product(BaseProduct):
    class Meta:
        app_label = 'stables_shop'

    long_description = models.TextField(blank=True, null=True)
