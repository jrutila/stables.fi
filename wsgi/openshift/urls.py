from django.conf.urls import patterns, include, url
from shop import urls as shop_urls
from stables_shop.views import NoShippingAddressCheckoutSelectionView
from stables_shop.views import ShopRedirectView
from django.http import HttpResponse
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from rest_framework import routers
#from stables.api import ParticipationViewSet

#router = routers.DefaultRouter()
#router.register(r'participations', ParticipationViewSet)

urlpatterns = patterns('',
    # Examples:
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^api-help/', 'views.api'),
    url(r'^shopper/checkout/$', NoShippingAddressCheckoutSelectionView.as_view()),
    url(r'^shopper/', include(shop_urls)),
    url(r'^shop/$', ShopRedirectView.as_view(), name='shop-in'),
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

from django.conf import settings
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))
