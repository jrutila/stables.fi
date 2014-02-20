from django.conf.urls import patterns, url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
            url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
            )

urlpatterns += staticfiles_urlpatterns()

urlpatterns += i18n_patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('cms.urls'))
)

