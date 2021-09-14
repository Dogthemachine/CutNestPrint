from django.shortcuts import get_object_or_404,render, redirect

from jsonview.decorators import json_view
from django.conf import settings

from apps.nest.models import Fashions, Items, ItemsSizes, ProducePage, Sizes, Pieces
from apps.orders.models import Orders, Rolls, ClothesInOrders
from apps.nest.forms import ItemForm, SizeForm, PieceForm, AvatarForm, ChooseRollForm
from apps.nest.helpers import TIFF2SVG
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile


def orders_page(request):

    all_orders = Orders.objects.all()

    if request.method == "POST":
        pass

    return render(
        request,
        "orders/orders_page.html", {
            'all_orders': all_orders,
        },
    )


def show_order(request, order_id):

    order = get_object_or_404(Orders, id=order_id)
    clothes = ClothesInOrders.objects.filter(order=order)

    if request.method == "POST":
        pass

    return render(
        request,
        "orders/show_order.html", {
            'clothes': clothes, 'order': order,
        },
    )

