from django.shortcuts import get_object_or_404,render, redirect

from jsonview.decorators import json_view
from django.conf import settings

from apps.nest.models import Fashions, Items, ItemsSizes, ProducePage, Sizes, Pieces
from apps.orders.models import Orders, Rolls, ClothesInOrders
from apps.nest.forms import ItemForm, SizeForm, PieceForm, AvatarForm, ChooseRollForm
from apps.nest.helpers import TIFF2SVG, MAKEBACKGROUND
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile

import sys
import os
import re
import random
import string
import shutil
from io import BytesIO
import datetime
from PIL import Image
import subprocess

def main_page(request):



    return render(
        request,
        "nest/main_page.html",
        {},
    )


def produce_page(request):

    produce_items = ProducePage.objects.all()
    amount_of_pieces = 0
    amount_of_items = 0
    for item in produce_items:
        amount_of_pieces += item.amount * item.items_sizes.get_pieces_amount()
        amount_of_items += item.amount
    if request.method == "POST":
        pass
    choose_roll_form = ChooseRollForm()

    return render(
        request,
        "nest/produce_page.html", {
            'produce_items': produce_items,
            'choose_roll_form': choose_roll_form,
            'amount_of_pieces': amount_of_pieces,
            'amount_of_items': amount_of_items,
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

        if 'change_avatar' in request.POST:
            avatar_form = AvatarForm(request.POST, request.FILES)
            file = request.FILES.get('image')
            if avatar_form.is_valid():
                nameimg2delete = item.image.path
                img = Image.open(file)
                temp = BytesIO()
                img.save(temp, "JPEG", quality=100)
                item.image = InMemoryUploadedFile(temp, None, item.image.path, 'image/jpeg', sys.getsizeof(temp), None)
                item.save()
                os.remove(nameimg2delete)
                temp.seek(0)
                return redirect('item_edit', item_id, 0)
            item_form = ItemForm(initial={'name': item.name, 'fashion': item.fashions.id})
            size_form = SizeForm()
            avatar_form = AvatarForm()

    else:
        item_form = ItemForm(initial={'name': item.name, 'fashion': item.fashions.id})
        size_form = SizeForm()
        piece_form = PieceForm()
        avatar_form = AvatarForm()

    return render(
        request,
        "nest/item_edit.html", {'item': item, 'item_form': item_form, 'size_form': size_form, 'piece_form': piece_form, 'avatar_form': avatar_form},
    )


@json_view
def produce_result_validate(request, roll_id):

    if request.method == "POST":

        roll = get_object_or_404(Rolls, id=roll_id)
        new_order = Orders()
        new_order.cost_rates = 3.2
        new_order.roll = roll
        count_of_items = 0
        for item in ProducePage.objects.all():
            count_of_items += item.amount
        new_order.amount_of_units = count_of_items
        new_order.amount_of_material = 0.0
        new_order.expected_cost = 0.0
        new_order.actual_cost = 0.0
        new_order.date_of_manufacture = datetime.datetime.now()
        new_order.save()
        for item in ProducePage.objects.all():
            new_unit = ClothesInOrders()
            new_unit.items_sizes = item.items_sizes
            new_unit.amount = item.amount
            new_unit.order = new_order
            new_unit.save()
        ProducePage.objects.all().delete()

        return {"success": True}

    else:
        return {"success": False}


@json_view
def produce_result_nesting(request, roll_id):

    if os.listdir(settings.MEDIA_RESULT_IMG):
        for file in os.listdir(settings.MEDIA_RESULT_IMG):
            os.remove(os.path.join(settings.MEDIA_RESULT_IMG, file))
    if os.listdir(settings.MEDIA_RESULT_CONTOUR):
        for file in os.listdir(settings.MEDIA_RESULT_CONTOUR):
            os.remove(os.path.join(settings.MEDIA_RESULT_CONTOUR, file))

    file_name = 1
    for item in ProducePage.objects.all():
        for piece in item.items_sizes.get_pieces():
            for i in range(item.amount):
                tif_name = settings.MEDIA_RESULT_IMG + "/" + str(file_name) + "UUU" + ".tif"
                shutil.copy(piece.detail.path, tif_name)
                if piece.contour:
                    contour_name = settings.MEDIA_RESULT_IMG + "/" + str(file_name) + ".svg"
                    shutil.copy(piece.contour.path, contour_name)
                else:
                    save_svg_path = settings.MEDIA_RESULT_CONTOUR + "/" + str(file_name) + ".svg"
                    TIFF2SVG(piece.detail.path, save_svg_path)
                file_name += 1

    MAKEBACKGROUND(500, 146)

    os.chdir("/Users/Dogthemachine/DeepNest/Deepnest")
    os.system("npm run start")

    return {"success": True}


def add_new_item(request):

    new = Items()
    new.cats_id = 10000
    new.name = _("New Item")
    new.added = datetime.datetime.now()
    new.fashions = Fashions.objects.filter(showcase_displayed=True)[0]
    temp = BytesIO()
    im = Image.open(str(settings.BASE_DIR) + "/assets/img/new_item_image.jpg")
    im.save(temp, "JPEG", quality=100)
    new.image = InMemoryUploadedFile(temp, None, ''.join(random.choice(string.ascii_letters + string.digits)for _ in range(18)), 'image/jpeg', sys.getsizeof(temp), None)
    new.save()

    return redirect('item_edit', new.id, 0)


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
        return render(
            request,
            "nest/items_list.html", {'items': items},
        )


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


@json_view
def delete_item(request, item_id):

    if request.method == "POST":
        item = get_object_or_404(Items, id=item_id)
        item.delete()

        return {"success": True}

    else:
        return {"success": False}


@json_view
def piece_rotate(request, piece_id):

    if request.method == "POST":
        piece = get_object_or_404(Pieces, id=piece_id)
        namedet2delete = piece.detail.path
        nameimg2delete = piece.image.path
        img = Image.open(piece.detail.path)
        img = img.rotate(90, expand=True)
        temp = BytesIO()
        img.save(temp, "TIFF", quality=100)
        piece.detail = InMemoryUploadedFile(temp, None, piece.detail.path, 'image/tiff', sys.getsizeof(temp), None)
        piece.save()
        os.remove(namedet2delete)
        os.remove(nameimg2delete)
        temp.seek(0)

        return {"success": True}

    else:
        return {"success": False}