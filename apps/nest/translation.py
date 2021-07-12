from modeltranslation.translator import translator, TranslationOptions

from apps.nest.models import Categories, Fashions, Items


class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name',)

class FashionsTranslationOptions(TranslationOptions):
    fields = ('name',)

class ItemsTranslationOptions(TranslationOptions):
    fields = ('name',)



translator.register(Categories, CategoriesTranslationOptions)
translator.register(Fashions, FashionsTranslationOptions)
translator.register(Items, ItemsTranslationOptions)

