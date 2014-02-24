from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django import db
from django.contrib.auth.models import User

TENANT_KEY='_tenant_id'

@receiver(user_logged_in)
def addTenantToSession(**kwargs):
    try:
        User.objects.get(pk=kwargs['user'].pk, username=kwargs['user'].username)
        kwargs['request'].session[TENANT_KEY] = db.connection.tenant.id
    except User.DoesNotExist:
        pass
