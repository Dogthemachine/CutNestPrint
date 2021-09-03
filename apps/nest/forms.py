from django import forms
from django.shortcuts import get_object_or_404,render
from django.utils.translation import gettext_lazy as _

from apps.nest.models import Fashions, Sizes, Items


class ItemForm(forms.Form):
    CHOICES = [(fashion.id, fashion.name) for fashion in Fashions.objects.filter(showcase_displayed=True)]
    name = forms.CharField(label=_('Item name'), max_length=250)
    fashion = forms.ChoiceField(label=_('Fashion'), widget=forms.Select, choices=CHOICES)


class SizeForm(forms.Form):
    SIZES = [(size.id, size.name) for size in Sizes.objects.all()]
    size = forms.ChoiceField(label=_('Add size'), widget=forms.Select, choices=SIZES)


class PieceForm(forms.Form):
    detail = forms.FileField(label=_('Select pieces'), widget=forms.ClearableFileInput(attrs={'multiple': True}))


# class AvatarForm(forms.Form):
#     image = forms.FileField(label=_('Item image'), widget=forms.ClearableFileInput())


class AvatarForm(forms.ModelForm):

    class Meta:
        model = Items
        fields = ('image', )

