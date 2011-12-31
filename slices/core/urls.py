from django.conf.urls.defaults import *

urlpatterns = patterns('slices.core.views',
    url( r'^list/$', 'list', name='list' ),
)
