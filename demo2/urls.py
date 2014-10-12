from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from demo2 import settings

from django.contrib import admin

urlpatterns = patterns('',
    # LOGIN AND REGISTER #
    url(r'^$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register/$', 'gift_search.views.register', name='register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    # PASSWORD RESET
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    'django.contrib.auth.views.password_reset_confirm',
    name='password_reset_confirm'),

    #All Gift Receivers for a given user#
    url(r'^receivers/$', 'gift_search.views.receivers', name='receivers'),
    #Populates initial page for a user after choosing a receiver#
    url(r'^receiver_page/(?P<receiver_id>\w+)/$', 'gift_search.views.receiver_page', name='receiver_page'),
    #Save Product Receiver -> POST request
    url(r'^receiver_page/(?P<receiver_id>\w+)/(?P<score>\w+)/(?P<asin>\w+)/$', 'gift_search.views.create_productreceiver', name='create_productreceiver'),
    #Update History -> GET request
    url(r'^update_history/(?P<receiver_id>\w+)/$', 'gift_search.views.update_history', name='update_history'),
    #Top Recommendations
    url(r'^top_recommendations/(?P<receiver_id>\w+)/$', 'gift_search.views.get_top_recommendations', name='get_top_recommendations'),




    # url(r'^get_gifts/(?P<receiver_id>\w+)/$', 'gift_search.views.get_gifts', name='get_gifts'),

    # PYTHON SOCIAL AUTH #
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
# (?P<date>.*)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)