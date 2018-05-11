# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from jsonfield import JSONField
from django.db import models
from django.utils import timezone


# import User model
from django.contrib.auth.models import User

# Create your models here.

class Map(models.Model):
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200)
    public = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    data = JSONField(null=True, blank=True)
    image = models.ImageField(upload_to=b'mapbuilder/%Y_%m_%d_%h_%M_%s', null=True,blank=True)
    published_date = models.DateTimeField(blank=True, null=True)


    def __unicode__(self):
        return self.name