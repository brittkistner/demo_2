from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'gift_search.views.home', name='home'),
    url(r'^friends/$', 'gift_search.views.friends', name='friends'),
    url(r'^get_gifts/(?P<receiver_id>\w+)$', 'gift_search.views.get_gifts', name='get_gifts'),

    # PYTHON SOCIAL AUTH #
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
