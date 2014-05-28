# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table(u'stables_shop_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_stables_shop.product_set', null=True, to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('unit_price', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=30, decimal_places=2)),
            ('long_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('stables_shop', ['Product'])

        # Adding model 'ProductActivator'
        db.create_table(u'stables_shop_productactivator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stables_shop.Product'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activators', to=orm['shop.Order'])),
            ('order_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.OrderItem'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal(u'stables_shop', ['ProductActivator'])

        # Adding model 'DigitalShippingAddressModel'
        db.create_table(u'stables_shop_digitalshippingaddressmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'stables_shop', ['DigitalShippingAddressModel'])

        # Adding model 'TicketProduct'
        db.create_table(u'stables_shop_ticketproduct', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stables_shop.Product'], unique=True, primary_key=True)),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stables.TicketType'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('duration', self.gf('durationfield.db.models.fields.duration.DurationField')(null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'stables_shop', ['TicketProduct'])

        # Adding model 'TicketProductActivator'
        db.create_table(u'stables_shop_ticketproductactivator', (
            (u'productactivator_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stables_shop.ProductActivator'], unique=True, primary_key=True)),
            ('start', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('end', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stables.RiderInfo'], null=True, blank=True)),
            ('duration', self.gf('durationfield.db.models.fields.duration.DurationField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'stables_shop', ['TicketProductActivator'])

        # Adding model 'EnrollProduct'
        db.create_table(u'stables_shop_enrollproduct', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stables_shop.Product'], unique=True, primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stables.Course'])),
            ('automatic_disable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'stables_shop', ['EnrollProduct'])

        # Adding model 'EnrollProductActivator'
        db.create_table(u'stables_shop_enrollproductactivator', (
            (u'productactivator_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stables_shop.ProductActivator'], unique=True, primary_key=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stables.RiderInfo'], null=True, blank=True)),
        ))
        db.send_create_signal(u'stables_shop', ['EnrollProductActivator'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'stables_shop_product')

        # Deleting model 'ProductActivator'
        db.delete_table(u'stables_shop_productactivator')

        # Deleting model 'DigitalShippingAddressModel'
        db.delete_table(u'stables_shop_digitalshippingaddressmodel')

        # Deleting model 'TicketProduct'
        db.delete_table(u'stables_shop_ticketproduct')

        # Deleting model 'TicketProductActivator'
        db.delete_table(u'stables_shop_ticketproductactivator')

        # Deleting model 'EnrollProduct'
        db.delete_table(u'stables_shop_enrollproduct')

        # Deleting model 'EnrollProductActivator'
        db.delete_table(u'stables_shop_enrollproductactivator')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'schedule.calendar': {
            'Meta': {'object_name': 'Calendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        },
        'schedule.event': {
            'Meta': {'object_name': 'Event'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Calendar']", 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'end_recurring_period': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Rule']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'schedule.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'shop.order': {
            'Meta': {'object_name': 'Order'},
            'billing_address_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cart_pk': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order_subtotal': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'}),
            'order_total': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'}),
            'shipping_address_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'shop.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_subtotal': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'}),
            'line_total': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['shop.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stables_shop.Product']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'product_reference': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'})
        },
        'stables.course': {
            'Meta': {'object_name': 'Course'},
            'allowed_levels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stables.RiderLevel']", 'symmetrical': 'False', 'blank': 'True'}),
            'course_fee': ('stables.models.financial.CurrencyField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'default_participation_fee': ('stables.models.financial.CurrencyField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['schedule.Event']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_participants': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'ticket_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stables.TicketType']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'stables.customerinfo': {
            'Meta': {'object_name': 'CustomerInfo'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'stables.riderinfo': {
            'Meta': {'object_name': 'RiderInfo'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stables.CustomerInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'levels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': "orm['stables.RiderLevel']"})
        },
        'stables.riderlevel': {
            'Meta': {'object_name': 'RiderLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'includes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['stables.RiderLevel']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'stables.tickettype': {
            'Meta': {'object_name': 'TicketType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'stables_shop.digitalshippingaddressmodel': {
            'Meta': {'object_name': 'DigitalShippingAddressModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'stables_shop.enrollproduct': {
            'Meta': {'object_name': 'EnrollProduct', '_ormbases': ['stables_shop.Product']},
            'automatic_disable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stables.Course']"}),
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stables_shop.Product']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'stables_shop.enrollproductactivator': {
            'Meta': {'object_name': 'EnrollProductActivator', '_ormbases': [u'stables_shop.ProductActivator']},
            u'productactivator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stables_shop.ProductActivator']", 'unique': 'True', 'primary_key': 'True'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stables.RiderInfo']", 'null': 'True', 'blank': 'True'})
        },
        'stables_shop.product': {
            'Meta': {'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_stables_shop.product_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'})
        },
        u'stables_shop.productactivator': {
            'Meta': {'object_name': 'ProductActivator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activators'", 'to': "orm['shop.Order']"}),
            'order_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.OrderItem']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stables_shop.Product']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        u'stables_shop.ticketproduct': {
            'Meta': {'object_name': 'TicketProduct', '_ormbases': ['stables_shop.Product']},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'duration': ('durationfield.db.models.fields.duration.DurationField', [], {'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stables_shop.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stables.TicketType']"})
        },
        u'stables_shop.ticketproductactivator': {
            'Meta': {'object_name': 'TicketProductActivator', '_ormbases': [u'stables_shop.ProductActivator']},
            'duration': ('durationfield.db.models.fields.duration.DurationField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'productactivator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stables_shop.ProductActivator']", 'unique': 'True', 'primary_key': 'True'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stables.RiderInfo']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['stables_shop']