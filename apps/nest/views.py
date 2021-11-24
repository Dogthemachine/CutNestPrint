from django.shortcuts import get_object_or_404,render, redirect

from jsonview.decorators import json_view
from django.conf import settings

from apps.nest.models import Fashions, Items, ItemsSizes, ProducePage, Sizes, Pieces
from apps.orders.models import Orders, Rolls, ClothesInOrders
from apps.nest.forms import ItemForm, SizeForm, PieceForm, AvatarForm, ChooseRollForm
from apps.nest.helpers import TIFF2SVG, MAKEBACKGROUND, SENDFILE, GETPOSITION, TIFF2BACKGROUND, CUTWHITESPACE
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template import loader
from apps.orders.models import GlobalSettings
from sys import platform

import dropbox
import json
import sys
import os
import random
import string
import shutil
from io import BytesIO
import datetime
from PIL import Image
import zipfile


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
            return redirect('item_edit', item_id, 0)
            size_form = SizeForm()
            piece_form = PieceForm()
            avatar_form = AvatarForm()

        if 'size' in request.POST:
            size_form = SizeForm(request.POST)
            if size_form.is_valid():
                size_id = size_form.cleaned_data.get('size')
                size = get_object_or_404(Sizes, id=size_id)
                if not ItemsSizes.objects.filter(items=item, sizes=size):
                    item_size = ItemsSizes(items=item, sizes=size)
                    item_size.save()
                return redirect('item_edit', item_id, 0)
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
            piece_form = PieceForm()
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
        new_order.cost_rates = 3.0
        new_order.roll = roll
        count_of_items = 0
        for item in ProducePage.objects.all():
            count_of_items += item.amount
        new_order.amount_of_units = count_of_items
        thepath = GlobalSettings.objects.all()[0]
        image = Image.open(thepath.jpeg_path)
        width, height = image.size
        material_amount = width / 2952.75
        new_order.amount_of_material = round(material_amount, 2)
        new_order.expected_cost = material_amount * new_order.cost_rates
        new_order.actual_cost = 0.0
        new_order.date_of_manufacture = datetime.datetime.now()
        temp = BytesIO()
        image.save(temp, "JPEG", quality=100)
        new_order.image_preview = InMemoryUploadedFile(temp, None, thepath.jpeg_path, 'image/jpeg', sys.getsizeof(image), None)
        new_order.save()
        temp.seek(0)
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
                tif_name = settings.MEDIA_RESULT_IMG + "/" + str(file_name) + ".tif"
                shutil.copy(piece.detail.path, tif_name)
                if piece.contour:
                    contour_name = settings.MEDIA_RESULT_IMG + "/" + str(file_name) + ".svg"
                    shutil.copy(piece.contour.path, contour_name)
                else:
                    save_svg_path = settings.MEDIA_RESULT_CONTOUR + "/" + str(file_name) + ".svg"
                    TIFF2SVG(piece.detail.path, save_svg_path)
                file_name += 1

    path_to_lust_order = MAKEBACKGROUND(1000, 146)
    globalsettings = GlobalSettings.objects.all()
    if globalsettings:
        globalsettings = globalsettings[0]
    else:
        globalsettings = GlobalSettings()
    globalsettings.result_tif_path = path_to_lust_order
    globalsettings.save()
    print('\n\n\n', globalsettings.result_tif_path, '\n\n\n')

    if platform == "darwin":
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
        return {"success": True,
                "amount": producepage.amount}

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

        c = {"piece": piece}
        t = loader.get_template('nest/piece.html')
        html = t.render(c, request)

        return {"success": True,
                "html": html
                }

    else:
        return {"success": False}


@json_view
def produce_result_finish_apportionment(request):

    if request.method == "POST":
        c = {}
        if os.path.exists(settings.MEDIA_RESULT_CONTOUR + "/exports.json"):
            gs = GlobalSettings.objects.all()[0]
            result_tif_path = gs.result_tif_path
            print('\n\n\n', result_tif_path, '\n\n\n')
            try:
                file = open(settings.MEDIA_RESULT_CONTOUR + "/exports.json")
                content = file.read()
                json_content = json.loads(content)
                for file in os.listdir(settings.MEDIA_RESULT_IMG):
                    open_tiff_path = os.path.join(settings.MEDIA_RESULT_IMG, file)
                    name = file.split(".")[0] + ".svg"
                    if name:
                        pos = GETPOSITION(json_content, name)
                        print("\n\n\n", "NAME= ", name, "ROT=", pos.rot, " X=", pos.x, " Y=", pos.y)
                        TIFF2BACKGROUND(open_tiff_path, result_tif_path, pos.x, pos.y, pos.rot)
            except:
                pass
            im = Image.open(result_tif_path)
            im = CUTWHITESPACE(im)
            save_jpeg_path = os.path.splitext(result_tif_path)[0] + ".jpg"
            im.save(result_tif_path, "TIFF")
            width, height = im.size
            width = int(width / 2)
            height = int(height / 2)
            size = width, height
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(save_jpeg_path, "JPEG")
            path_to_show = "result_orders/" + save_jpeg_path.split("/")[-1]
            gs.jpeg_path = save_jpeg_path
            gs.save()
            c = {"image": path_to_show}
        t = loader.get_template('nest/apportionment.html')
        html = t.render(c, request)


    return {"success": True, "html": html}


@json_view
def produce_result_send_email(request, roll_id):

    if request.method == "POST":
        if os.path.exists(settings.MEDIA_RESULT_CONTOUR + "/exports.json"):

            # make path to lust order/tiff
            globalsettings = GlobalSettings.objects.all()
            if globalsettings:
                globalsettings = globalsettings[0]
            path_to_lust_order_tif = globalsettings.result_tif_path
            # make a name for new zip file
            zip_file_path = settings.MEDIA_RESULT_IMG + "/one_more.zip"
            # make an ZipFile object
            zipFile = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
            # add tiff file to zip
            zipFile.write(path_to_lust_order_tif)
            # close
            zipFile.close()

            class TransferData:
                def __init__(self, access_token):
                    self.access_token = access_token

                def upload_file(self, file_from, file_to):
                    """upload a file to Dropbox using API v2"""
                    dbx = dropbox.Dropbox(self.access_token)
                    with open(file_from, 'rb') as f:
                        dbx.files_upload(f.read(), file_to)

            def main():
                access_token = '2HHk-EYa2tQAAAAAAAAAAS6m-xE3n5XvRSCj-nQ-T5M7Kxx8hBrpwkaHseaK9D0_'
                transferData = TransferData(access_token)
                dbx = dropbox.Dropbox(access_token)
                # The full path to upload the file to, including the file name
                file_to = '/CNP/one_more.zip'
                # Delete old file from Dropbox
                try:
                    dbx.files_delete(file_to)
                except:
                    pass
                # API v2
                transferData.upload_file(zip_file_path, file_to)
                # Create sheared link for file?
                shared_link_metadata = dbx.sharing_create_shared_link_with_settings("/CNP/one_more.zip")
                return shared_link_metadata.url

            message_text = main()

            # making massage
            print("SENDING EMAIL")
            password = "Bonanzzza789"
            from_address = "catcult.club@gmail.com"
            to_address = "uabitex@gmail.com"
            SENDFILE(password, from_address, to_address, message_text)

    return {"success": True}