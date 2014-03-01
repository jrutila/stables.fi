from django.contrib import admin
from models import TicketProduct

#if tenant_schemas.utils.connection.get_tenant().schema_name == 'public':
admin.site.register(TicketProduct)
