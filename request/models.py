# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class request(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.CharField(max_length = 11)
    requestorname = models.CharField(max_length = 100)
    requestorempid = models.CharField(max_length = 10)
    requesteddate = models.DateField(auto_now_add=True, blank=True)
    projectname = models.CharField(max_length = 100)
    process = models.CharField(max_length = 100)
    description = models.CharField(max_length = 2000)
    processoverview = models.CharField(max_length = 300, blank=True) 
    excepted_TAT = models.DateTimeField(blank=True)
    requestormanagername = models.CharField(max_length = 100)
    requestormanagermailid = models.CharField(max_length = 100)
    requestormailid = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100)
    comments = models.CharField(max_length = 300, blank=True)
    document = models.FileField(upload_to='documents/', blank=True)
    
    