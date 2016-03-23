# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from datetime import timezone


from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from .models import Contact, Message, Report


class ChatDetail(CsrfExemptMixin, LoginRequiredMixin, ListView):

    context_object_name = 'user_message_list'
    template_name = 'django_simple_chat/chat_detail.html'

    def get_queryset(self):
        # self.id = get_object_or_404(settings.AUTH_USER_MODEL, id=self.request.user.id)
        # print(self.id)
        return Contact.objects.all()


class ChatOverview(CsrfExemptMixin, LoginRequiredMixin, ListView):

    context_object_name = 'contacts'
    template_name = 'django_simple_chat/chat_overview.html'

    def get_user_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_queryset(self):
        self.user_object = self.get_user_object()
        return Contact.add_last_message(self.user_object)

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            body = request.body.decode(encoding='UTF-8')
            body = json.loads(body)
            message = body['message']
            messenger = get_object_or_404(User, id=self.request.user.id)
            print(self.get_queryset()[0].receiver.id)
            receiver_id = self.get_queryset()[0].receiver.id
            receiver = get_object_or_404(User, id=receiver_id)
            Message.add_message(messenger, receiver, message)
            return JsonResponse({'status': 200})

    def get_context_data(self, **kwargs):
        context = super(ChatOverview, self).get_context_data(**kwargs)
        lastest_contact = self.get_queryset()[-1]
        user_obj = self.get_user_object()
        main_messages_sent = Message.objects.filter(messenger=user_obj, receiver=lastest_contact)
        main_messages_received = Message.objects.filter(messenger=lastest_contact, receiver=user_obj)

        main_messages = main_messages_sent | main_messages_received

        context['main_messages'] = main_messages
        return context