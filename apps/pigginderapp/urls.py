from django.conf.urls import url
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^register_processing$', views.register_processing),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^last_confirmation$', views.last_confirmation),
    url(r'^last_info_processing$', views.last_info_processing),
    url(r'^profile$', views.profile),
    url(r'^editing_profile$', views.editing_profile),
    url(r'^pick/(?P<piggie_id>\d+)$', views.pick),
    url(r'^bye/(?P<piggie_id>\d+)$', views.bye),
    url(r'^like/(?P<piggie_id>\d+)$', views.like),
    url(r'^matched_with/(?P<piggie_id>\d+)$', views.matched_with),
    url(r'^matched_result$', views.matched_result),
    url(r'^friendzoning/(?P<piggie_id>\d+)$', views.friendzone),
    url(r'^likingback/(?P<piggie_id>\d+)$', views.likingback),
    url(r'^message/(?P<piggie_id>\d+)$', views.message),
    url(r'^message/processing/(?P<piggie_id>\d+)$', views.messaging),
    url(r'^message_page/(?P<piggie_id>\d+)$', views.message_page),
    url(r'^messagingback/(?P<piggie_id>\d+)$', views.messagingback),

]
