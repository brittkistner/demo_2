from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'gift_search.views.home', name='home'),
    #All Gift Receivers for a given user#
    url(r'^receivers/$', 'gift_search.views.receivers', name='receivers'),
    #Populates initial page for a user after choosing a receiver#
    url(r'^receiver_page/(?P<receiver_id>\w+)/$', 'gift_search.views.receiver_page', name='receiver_page'),
    url(r'^receiver_page/(?P<receiver_id>\w+)/(?P<score>\w+)/(?P<asin>\w+)/', 'gift_search.views.create_productreceiver', name='create_productreceiver'),



    url(r'^get_gifts/(?P<receiver_id>\w+)/$', 'gift_search.views.get_gifts', name='get_gifts'),

    # PYTHON SOCIAL AUTH #
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
# (?P<date>.*)