from django.conf.urls.defaults import *

# URLs here will define which RxtxManager plug-in are enable for this set up.
urlpatterns = patterns('automations',
    url(r'^status/$',                           'status.index',     name='automations-status'),
    url(r'^status/delete/(?P<chain_id>\d+)/$',  'status.delete',    name='automations-delete-chain'),
    url(r'^status/retry/(?P<chain_id>\d+)/$',   'status.retry',     name='automations-retry-chain'),
    url(r'^list/$',                             'list.index',       name='automations-list'),
    url(r'^list/edit/(?P<auto_id>\d+)/$',       'list.edit',        name='automations-edit'),
    url(r'^list/add/$',                         'list.add',         name='automations-add'),
)
