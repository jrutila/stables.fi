from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from rest_framework import routers
#from stables.api import ParticipationViewSet

#router = routers.DefaultRouter()
#router.register(r'participations', ParticipationViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^', 'public_views.home'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
