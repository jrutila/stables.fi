from django.contrib import admin
from models import TicketProduct
from models import TicketProductActivator
from models import EnrollProduct
from models import EnrollProductActivator

#if tenant_schemas.utils.connection.get_tenant().schema_name == 'public':
admin.site.register(TicketProduct)
admin.site.register(TicketProductActivator)
admin.site.register(EnrollProduct)
admin.site.register(EnrollProductActivator)
