# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


from django.db import models
from django_fsm import FSMField, transition
from structlog import get_logger


class Network(models.Model):
    name = models.CharField(max_length=100, unique=True)
    prefix = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=50, default='')
    client_wsdl = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'network'

    def __unicode__(self):
        return u'{0}'.format(self.name)


class SmsMessage(models.Model):
    # Define State Machine
    received, started, failed, submitted, completed = "received", "started", "failed", "submitted", "completed"  # noqa
    STATE_CHOICES = (
        (received, received),
        (started, started),
        (failed, failed),
        (submitted, submitted),
        (completed, completed),
    )

    message_id = models.CharField(max_length=50)
    sender_id = models.CharField(max_length=50, default='')
    msisdn = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
    priority = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='')
    state = FSMField(default=received, choices=STATE_CHOICES, protected=True)
    callback = models.CharField(max_length=200, default='')
    network = models.ForeignKey(Network, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sms_message'

    def __unicode__(self):
        return self.message_id

    @transition(field=state, source=['received', 'failed'], target=started)
    def started(self):
        '''
        Change message request to started state.
        '''
        logger = get_logger(__name__).bind(message_id=self.message_id)
        logger.info("state_transition", from_="received", to="started")
        return

    @transition(field=state, source='*', target=failed)
    def failed(self):
        '''
        For started requests that cannot be submitted to Network
        hence in a failed state.
        '''
        logger = get_logger(__name__).bind(message_id=self.message_id)
        logger.info("state_transition", from_="started", to="failed")
        return

    @transition(field=state, source='started', target=submitted)
    def submitted(self):
        '''
        Change message request to submitted state.
        '''
        logger = get_logger(__name__).bind(message_id=self.message_id)
        logger.info("state_transition", from_="started", to="submitted")
        return

    @transition(field=state, source=['submitted', 'failed'], target=completed)
    def completed(self):
        '''
        Request was sucessfully submited to mno and a response returned.
        '''
        logger = get_logger(__name__).bind(message_id=self.message_id)
        logger.info("state_transition", from_="submitted", to="completed")
        return
