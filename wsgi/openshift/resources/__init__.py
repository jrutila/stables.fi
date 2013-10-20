from import_export import resources

from stables.models import Horse
from django.contrib.auth.models import User
from stables.models import UserProfile, RiderInfo, CustomerInfo, RiderLevel
from stables.models import InstructorInfo, Course, Participation, Enroll
from stables.models import Ticket, Transaction, TicketType
from stables.models import Accident, AccidentType
from schedule.models import Calendar, Event, Rule

from datetime import datetime, timedelta

class HorseResource(resources.ModelResource):
  class Meta:
    model = Horse
    fields = ('id', 'name', 'last_usage_date')

class UserResource(resources.ModelResource):
  class Meta:
    model = User

class UserProfileResource(resources.ModelResource):
  class Meta:
    model = UserProfile

class RiderInfoResource(resources.ModelResource):
  class Meta:
    model = RiderInfo

class CustomerInfoResource(resources.ModelResource):
  class Meta:
    model = CustomerInfo

class InstructorInfoResource(resources.ModelResource):
  class Meta:
    model = InstructorInfo

class RiderLevelResource(resources.ModelResource):
  class Meta:
    model = RiderLevel

class CourseResource(resources.ModelResource):
  class Meta:
    model = Course
    
class CalendarResource(resources.ModelResource):
  class Meta:
    model = Calendar

class EventResource(resources.ModelResource):
  class Meta:
    model = Event
  def save_instance(self, instance, dry_run=False):
      super(Event, instance).save()

class RuleResource(resources.ModelResource):
  class Meta:
    model = Rule

class ParticipationResource(resources.ModelResource):
  class Meta:
    model = Participation

  def get_queryset(self):
    qs = resources.ModelResource.get_queryset(self)
    return qs.filter(start__gte=datetime.now()-timedelta(weeks=2))

  def save_instance(self, instance, dry_run=False):
    self.before_save_instance(instance, dry_run)
    if not dry_run:
      instance.save(omitstatechange=True)
    self.after_save_instance(instance, dry_run)


class EnrollResource(resources.ModelResource):
  class Meta:
    model = Enroll

from import_export import fields
from django.contrib.contenttypes.models import ContentType
class ContentTypeField(fields.Field):
    def clean(self, data):
        ctapp, ctmodel = data[self.column_name].split('.')
        value = ContentType.objects.get(app_label=ctapp, model=ctmodel)
        return value

    def get_value(self, obj):
        try:
            value = getattr(obj, self.attribute)
        except ContentType.DoesNotExist:
            return ""
        if not value:
            return ""
        return value.app_label+"."+value.model

class TicketResource(resources.ModelResource):
  class Meta:
    model = Ticket

  def get_queryset(self):
    qs = resources.ModelResource.get_queryset(self)
    return qs.exclude(transaction__created_on__lt=datetime.now()-timedelta(weeks=2))

  owner_type = ContentTypeField(column_name="owner_type_id", attribute="owner_type")

class TicketTypeResource(resources.ModelResource):
  class Meta:
    model = TicketType

class TransactionResource(resources.ModelResource):
  content_type = ContentTypeField(column_name="content_type_id", attribute="content_type")

  class Meta:
    model = Transaction

  def get_queryset(self):
    qs = resources.ModelResource.get_queryset(self)
    return qs.filter(created_on__gte=datetime.now()-timedelta(weeks=2))

class AccidentResource(resources.ModelResource):
  class Meta:
    model = Accident

from stables.models import LocalizedText
class I18NCharField(fields.Field):
    def clean(self, data):
        return LocalizedText(eval(data[self.column_name]))

    def get_value(self, obj):
        value = getattr(obj, self.attribute)
        if not isinstance(value, LocalizedText):
            return value
        return unicode(value.texts)

class AccidentTypeResource(resources.ModelResource):
  class Meta:
    model = AccidentType
  name = I18NCharField(column_name="name", attribute="name")
