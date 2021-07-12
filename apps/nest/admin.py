from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from apps.nest.models import Categories, Fashions, Items, Sizes, Pieces


class CategoriesAdmin(TranslationAdmin):
    list_display = ('name', 'sequence',)

class FashionsAdmin(TranslationAdmin):
    list_display = ('name', 'sequence',)

class SizesAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ItemsAdmin(TranslationAdmin):
    list_display = ('name',)

class PiecesAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Fashions, FashionsAdmin)
admin.site.register(Sizes, SizesAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register(Pieces, PiecesAdmin)