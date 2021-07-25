from django.shortcuts import render

from apps.nest.models import Fashions

def main_page(request):



    return render(
        request,
        "nest/main_page.html",
        {},
    )


def produce_page(request):

    return render(
        request,
        "nest/produce_page.html", {},
    )


def fashions_page(request):

    fashions = Fashions.objects.all()

    return render(
        request,
        "nest/fashions_page.html", {'fashions': fashions},
    )


def new_item(request):
    return render(
        request,
        "nest/new_item_page.html", {},
    )


def fashions_list(request, fashion_id):
    return render(
        request,
        "nest/fashions_list.html", {},
    )