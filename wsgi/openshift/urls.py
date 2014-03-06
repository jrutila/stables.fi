from django.conf.urls import patterns, include, url
from shop import urls as shop_urls
from stables_shop.views import NoShippingAddressCheckoutSelectionView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from rest_framework import routers
#from stables.api import ParticipationViewSet

#router = routers.DefaultRouter()
#router.register(r'participations', ParticipationViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^api-help/', 'views.api'),
    url(r'^shop/checkout/$', NoShippingAddressCheckoutSelectionView.as_view()),
    url(r'^shop/', include(shop_urls)),
    url(r'^s/', include('stables_shop.urls')),
    url(r'^', include('stables.urls')),

    url(r'^comments/', include('fluent_comments.urls')),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^api/', include(router.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
