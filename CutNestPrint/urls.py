"""CutNestPrint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from apps.nest.views import produce_page, fashions_page, new_item, items_list, produce_add, produce_del, item_edit, \
    item_size_del, piece_del, produce_result, add_new_item

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", fashions_page, name="main_page"),
    path("fashions/", fashions_page, name="fashions_page"),
    path("new/", add_new_item, name="add_new_item"),
    path("items_list/<int:fashion_id>/", items_list, name="items_list"),
    path("produce/", produce_page, name="produce_page"),
    path("produce-add/<int:imagesize_id>/<int:amount>/", produce_add, name="produce_add"),
    path("produce-del/<int:imagesize_id>/", produce_del, name="produce_del"),
    path("produce_result/", produce_result, name="produce_result"),
    path("item_edit/<int:item_id>/<int:size_id>/", item_edit, name="item_edit"),
    path("item-size-del/<int:item_id>/<int:size_id>/", item_size_del, name="item_size_del"),
    path("piece-del/<int:piece_id>/", piece_del, name="piece_del"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]