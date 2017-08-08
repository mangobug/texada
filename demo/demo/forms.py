# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.widgets import DateTimeInput

from .models import Product

from datetime import datetime

from bootstrap3.tests import TestForm


class ProductForm(forms.Form):
    """
    Product Search Form
    """
    start_date = forms.DateTimeField(
                                initial=datetime.now(),
                                label="Starting From",
                                widget=DateTimeInput(),
    )
    end_date = forms.DateTimeField(
                                initial=datetime.now(),
                                label="Ending At",
                                widget=DateTimeInput(),
    )


class UploadFileForm(forms.Form):
    """
    Form to upload initial data into the system
    """
    file = forms.FileField()
