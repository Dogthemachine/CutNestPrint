from django.shortcuts import get_object_or_404,render, redirect

from jsonview.decorators import json_view

from apps.nest.models import Fashions, Items, ItemsSizes, ProducePage, Sizes, Pieces
from apps.nest.forms import ItemForm, SizeForm, PieceForm

from django.conf import settings

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


def item_edit(request, item_id, size_id):

    item = get_object_or_404(Items, id=item_id)

    if request.method == 'POST':
        if 'name' in request.POST:
            item_form = ItemForm(request.POST)
            if item_form.is_valid():
                name = item_form.cleaned_data.get('name')
                fashion_id = item_form.cleaned_data.get('fashion')
                fashion = get_object_or_404(Fashions, id=fashion_id)
                item.name = name
                item.fashions = fashion
                item.save()
            size_form = SizeForm()
            piece_form = PieceForm()

        if 'size' in request.POST:
            size_form = SizeForm(request.POST)
            if size_form.is_valid():
                size_id = size_form.cleaned_data.get('size')
                size = get_object_or_404(Sizes, id=size_id)
                if not ItemsSizes.objects.filter(items=item, sizes=size):
                    item_size = ItemsSizes(items=item, sizes=size)
                    item_size.save()
            item_form = ItemForm(initial={'name': item.name, 'fashion': item.fashions.id})
            piece_form = PieceForm()

        if size_id != 0 and 'piece' in request.POST or 'add_piece' in request.POST:
            piece_form = PieceForm(request.POST, request.FILES)
            files = request.FILES.getlist('detail')
            if piece_form.is_valid():
                for f in files:
                    main, sub = f.content_type.split('/')
                    if main in ["image"] and sub == 'tiff':
                        item_size = get_object_or_404(ItemsSizes, id=size_id)
                        p = Pieces(items_sizes=item_size, detail=f)
                        p.save()
                return redirect('item_edit', item_id, 0)
                # piece_form.save(size_id)
            item_form = ItemForm(initial={'name': item.name, 'fashion': item.fashions.id})
            size_form = SizeForm()

    else:
        item_form = ItemForm(initial={'name': item.name, 'fashion': item.fashions.id})
        size_form = SizeForm()
        piece_form = PieceForm()

    return render(
        request,
        "nest/item_edit.html", {'item': item, 'item_form': item_form, 'size_form': size_form, 'piece_form': piece_form},
    )


@json_view
def produce_result(request):

    print("PRIVET")
    if request.method == "POST":
        for item in ProducePage.objects.all():
            print("trying to collect items:", item.id)
            for piece in item.items_sizes.get_pieces():
                print("trying to save piece with id:", piece.id)

        return {"success": True}

    else:
        return {"success": False}


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


@json_view
def item_size_del(request, item_id, size_id):

    if request.method == "POST":
        item = get_object_or_404(Items, id=item_id)
        size = get_object_or_404(Sizes, id=size_id)
        ItemsSizes.objects.filter(items=item, sizes=size).delete()
        return {"success": True}

    else:
        return {"success": False}


@json_view
def piece_del(request, piece_id):

    if request.method == "POST":
        item = get_object_or_404(Pieces, id=piece_id)
        item.delete()
        return {"success": True}

    else:
        return {"success": False}