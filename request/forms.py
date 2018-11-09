from django.forms import ModelForm
from django import forms
from models import request
from django.contrib.admin import widgets


class createRequest(ModelForm):
    class Meta:
        model = request
        fields = ['requestorname', 'requestorempid', 'requestid', 'projectname', 'process', 'description','processoverview', 'excepted_TAT', 'requestormanagername', 'requestormanagermailid', 'requestormailid', 'document']
        
