from django import forms
from django.shortcuts import get_object_or_404,render
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Orders, ClothesInOrders, MaterialTypes, Rolls


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

