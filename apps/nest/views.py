from django.shortcuts import render

def main_page(request):



    return render(
        request,
        "nest/main_page.html",
        {
            # "category": category,
            # "categories": categories,
            # "fashion": fashion,
            # "fashions": fashions,
            # "items": items,
            # "itm": itm,
            # "artist": artist,
            # "title_tag": title_tag,
            # "description_tag": description_tag,
        },
    )