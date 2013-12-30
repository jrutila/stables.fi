import os
from django.core.management.base import BaseCommand
from django.db import connection
from optparse import make_option
from tenant_schemas.utils import get_tenant_model
import datetime
from import_export import resources

dt = datetime.timedelta(weeks=2)

def get_participation_queryset(self):
    qs = resources.ModelResource.get_queryset(self)
    return qs.filter(start__gte=datetime.datetime.now()-dt)

def get_ticket_queryset(self):
    qs = resources.ModelResource.get_queryset(self)
    return qs.exclude(transaction__created_on__lt=datetime.datetime.now()-dt)

def get_transaction_queryset(self):
    qs = resources.ModelResource.get_queryset(self)
    return qs.filter(created_on__gte=datetime.datetime.now()-dt)

querysets = {
        "ParticipationResource": get_participation_queryset,
        "TicketResource": get_ticket_queryset,
        "TransactionResource": get_transaction_queryset,
        }

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option("-d", "--data", dest="datadir"),
            make_option("-s", "--schema", dest="schema"),)

    def handle(self, *args, **kwargs):
        tenant = connection.tenant
        if not tenant and kwargs['schema']:
            tenant = get_tenant_model().objects.get(schema_name=kwargs['schema'])
        print "Exporting %s..." % tenant

        connection.set_tenant(tenant, include_public=False)

        datadir=kwargs['datadir']

        if not os.path.exists(datadir):
            os.mkdir(datadir)

        mod = __import__('resources')


        for m in mod.__dict__.items():
            if 'Resource' in m[0]:
                mname = m[0]
                print mname
                res = m[1]
                if mname in querysets:
                    res.get_queryset = querysets[mname]
                dataset=res().export()
                f = open(os.path.join(datadir, '%s.csv' % mname), 'w')
                f.write(dataset.csv)
 
