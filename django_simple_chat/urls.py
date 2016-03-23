# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import ChatDetail, ChatOverview  # , chat_new, chat_overview

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)$', ChatDetail.as_view(), name='ChatDetail'),
    # url(r'^~new/$', chat_new, name='new'),
    url(r'^', ChatOverview.as_view(), name='ChatOverview'),
]
