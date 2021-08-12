from django.shortcuts import get_object_or_404,render

from jsonview.decorators import json_view

from apps.nest.models import Fashions, Items, ItemsSizes, ProducePage

def main_page(request):



    return render(
        request,
        "nest/main_page.html",
        {},
    )


def produce_page(request):

    produce_items = ProducePage.objects.all()

    return render(
        request,
        "nest/produce_page.html", {
            'produce_items': produce_items
        },
    )


def fashions_page(request):

    # fashions = Fashions.objects.all()
    fashions = Fashions.objects.filter(showcase_displayed=True)

    return render(
        request,
        "nest/fashions_page.html", {'fashions': fashions},
    )


def new_item(request):
    return render(
        request,
        "nest/new_item_page.html", {},
    )


def items_list(request, fashion_id):

    items = Items.objects.filter(fashions__id=fashion_id)

    return render(
        request,
        "nest/items_list.html", {'items': items},
    )


@json_view
def produce_add(request, imagesize_id, amount):

    if request.method == "POST":
        imagesize = get_object_or_404(ItemsSizes, id=imagesize_id)
        producepage = ProducePage.objects.filter(items_sizes=imagesize)
        if producepage:
            producepage = producepage[0]
            producepage.amount += amount
        else:
            producepage = ProducePage()
            producepage.amount = amount
            producepage.items_sizes = imagesize
        producepage.save()
        return {"success": True}

    else:
        return {"success": False}


@json_view
def produce_del(request, imagesize_id):

    if request.method == "POST":
        imagesize = get_object_or_404(ItemsSizes, id=imagesize_id)
        ProducePage.objects.filter(items_sizes=imagesize).delete()
        return {"success": True}

    else:
        return {"success": False}