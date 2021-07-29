from django import template
from django.utils.safestring import mark_safe

from apps.nest.models import ProducePage

register = template.Library()


@register.simple_tag
def get_produce_amount():
    produce_amount = 0
    for produce in ProducePage.objects.all():
        produce_amount += produce.amount
    return mark_safe(produce_amount)
