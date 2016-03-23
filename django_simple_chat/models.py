# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone




class Contact(models.Model):
    messenger = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="messenger")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="receiver")
    deleted = models.IntegerField(_("Deleted"), default=0)
    blocked = models.IntegerField(_("Blocked"), default=0)
    unread = models.IntegerField(_("Unread"), default=0)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def add_last_message(user):
        contacts = Contact.objects.filter(messenger=user, deleted=0, blocked=0)
        contact_list = []

        for contact in contacts:
            contacts = get_object_or_404(User, id=user.id)
            contact_list += User.objects.filter(id=contact.receiver.id)

        for contact in contact_list:
            last_sent = Message.objects.filter(messenger=user, receiver=contact.id).last()
            last_received = Message.objects.filter(messenger=contact.id, receiver=user).last()

            if last_sent:
                if last_received:
                    if last_sent.time_sent < last_received.time_sent:
                        contact.last_message = last_received
                    else:
                        contact.last_message = last_sent
                else:
                    contact.last_message = last_sent
            else:
                if last_received:
                    contact.last_message = last_received
                else:
                    contact.last_message = ""
        return contact_list

    def __str__(self):
        return self.receiver.username


class Message(models.Model):
    messenger = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="message_messenger")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="message_receiver")
    message = models.TextField(_("Message"), blank=True)
    time_sent = models.DateTimeField(default=timezone.now)
    time_read = models.DateTimeField(blank=True, null=True)

    def add_message(messenger, receiver, message):
        Message.objects.create(messenger=messenger, receiver=receiver, message=message)

    def __str__(self):
        return self.message


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reporter")
    reported = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reported")
    time_sent = models.DateTimeField(default=timezone.now)
    messsage = models.TextField(_("Message"), blank=True)

    def __str__(self):
        return self.message
