from django import forms
from django.shortcuts import get_object_or_404,render
from django.utils.translation import gettext_lazy as _

from apps.nest.models import Fashions, Sizes, Items
from apps.orders.models import Rolls


class ItemForm(forms.Form):
    CHOICES = [(fashion.id, fashion.name) for fashion in Fashions.objects.filter(showcase_displayed=True)]
    name = forms.CharField(label=_('Item name'), max_length=250)
    fashion = forms.ChoiceField(label=_('Fashion'), widget=forms.Select, choices=CHOICES)


class SizeForm(forms.Form):
    # SIZES = []
    # for item in [(size.id, size.name) for size in Sizes.objects.all()]:
    #     SIZES.append(item[1])
    # SIZES = list(set(SIZES))
    SIZES = [(size.id, size.name) for size in Sizes.objects.all()]
    size = forms.ChoiceField(label=_('Add size'), widget=forms.Select, choices=SIZES)


# class SizeForm(forms.Form):
#     size = forms.ChoiceField(label=_('Add size'), widget=forms.Select)
#
#     def init(self, *args, **kwargs):
#         if 'fashion_id' in kwargs:
#             fashion_id = kwargs.pop('fashion_id')
#         else:
#             fashion_id = 0
#         super(SizeForm, self).init(*args, **kwargs)
#         if fashion_id > 0:
#             self.fields['size'].choices = [(size.id, size.name) for size in Sizes.objects.filter(fachion__id=fashion_id)]


class PieceForm(forms.Form):
    detail = forms.FileField(label=_('Select pieces'), widget=forms.ClearableFileInput(attrs={'multiple': True}))


class AvatarForm(forms.ModelForm):

    class Meta:
        model = Items
        fields = ('image', )


class ChooseRollForm(forms.Form):
    ROLLS = [(roll.id, roll.material_type.name + " (" + str(roll.actual_meters) + "m)") for roll in Rolls.objects.all()]
    roll = forms.ChoiceField(label=_('Choose roll'), widget=forms.Select, choices=ROLLS)


