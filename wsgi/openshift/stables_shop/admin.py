from django.contrib import admin
from models import TicketProduct
from models import TicketProductActivator

#if tenant_schemas.utils.connection.get_tenant().schema_name == 'public':
admin.site.register(TicketProduct)
admin.site.register(TicketProductActivator)
