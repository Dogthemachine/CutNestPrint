from django.contrib import admin
from apps.nest.models import Categories, Fashions, Items, Sizes, Pieces


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'sequence',)

class FashionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'sequence',)

class SizesAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PiecesAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Fashions, FashionsAdmin)
admin.site.register(Sizes, SizesAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register(Pieces, PiecesAdmin)
