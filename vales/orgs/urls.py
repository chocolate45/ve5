# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.core.urlresolvers import reverse, reverse_lazy

from . import views


urlpatterns = [
    # Org patterns
    url(
        regex=r'^$',
        view=views.OrgListView.as_view(),
        name='org_list'
    ),
    # url(
    #     regex=r'^~redirect/$',
    #     view=views.OrgRedirectView.as_view(),
    #     name='redirect'
    # ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/$',
        view=views.OrgDetailView.as_view(),
        name='org_detail'
    ),
    url(
        regex=r'^~create-org/$',
        view=views.OrgCreateView.as_view(),
        name='org_create'
    ),
    url(
        regex=r'^~update-org/(?P<slug>[\w.@+-]+)/$',
        view=views.OrgUpdateView.as_view(),
        name='org_update'
    ),
    # Profile patterns
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/members/$',
        view=views.ProfileListView.as_view(),
        name='profile_list'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/join/(?P<username>[\w.@+-]+)/create-profile/$',
        view=views.ProfileCreateView.as_view(),
        name='profile_create'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/(?P<username>[\w.@+-]+)/update-profile/(?P<pk>[0-9]+)$',
        view=views.ProfileUpdateView.as_view(),
        name='profile_update'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/(?P<username>[\w.@+-]+)/profile/(?P<pk>[\d+-]+)$',
        view=views.ProfileDetailView.as_view(),
        name='profile_detail'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/(?P<username>[\w.@+-]+)/profile-created/$',
        view=views.ProfileSuccessView.as_view(),
        name='profile_success'
    ),
]
