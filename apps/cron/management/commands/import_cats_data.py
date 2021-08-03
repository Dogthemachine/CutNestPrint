from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.nest.models import Categories, Fashions, Sizes, Items, ItemsSizes
from apps.cats.models import Categories as CatsCategories
from apps.cats.models import Fashions as CatsFashions
from apps.cats.models import Sizes as CatsSizes
from apps.cats.models import Items as CatsItems
from apps.cats.models import Balance as CatsBalance


class Command(BaseCommand):
    help = "Import data from cats database."

    def handle(self, *args, **options):
        print(timezone.now())

        for cats_category in CatsCategories.objects.using('cats').all():
            try:
                Categories.objects.get(cats_id=cats_category.id)
            except Categories.DoesNotExist:
                print(cats_category.name)
                category = Categories()
                category.cats_id = cats_category.id
                category.name = cats_category.name
                category.image = cats_category.image
                category.image_hover = cats_category.image_hover
                category.sequence = cats_category.sequence
                category.save()

        for cats_fashion in CatsFashions.objects.using('cats').all():
            try:
                Fashions.objects.get(cats_id=cats_fashion.id)
            except Fashions.DoesNotExist:
                print(cats_fashion.name)
                try:
                    category = Categories.objects.get(cats_id=cats_fashion.categories.id)
                except Categories.DoesNotExist:
                    print('----- category error ----', cats_fashion.categories.name)
                    continue
                fashion = Fashions()
                fashion.cats_id = cats_fashion.id
                fashion.categories = category
                fashion.name = cats_fashion.name
                fashion.image = cats_fashion.image
                fashion.image_hover = cats_fashion.image_hover
                fashion.sequence = cats_fashion.sequence
                fashion.save()

        for cats_size in CatsSizes.objects.using('cats').all():
            try:
                Sizes.objects.get(cats_id=cats_size.id)
            except Sizes.DoesNotExist:
                print(cats_size.name)
                try:
                    category = Categories.objects.get(cats_id=cats_size.categories.id)
                except Categories.DoesNotExist:
                    print('----- category error ----', cats_size.categories.name)
                    continue
                size = Sizes()
                size.cats_id = cats_size.id
                size.categories = category
                size.name = cats_size.name
                size.description = cats_size.description
                size.sequence = cats_size.sequence
                size.save()
        item_name = ''
        for cats_item in CatsItems.objects.using('cats').all().order_by('fashions','name'):
            if item_name == cats_item.name:
                continue
            item_name = cats_item.name
            try:
                Items.objects.get(cats_id=cats_item.id)
            except Items.DoesNotExist:
                print(cats_item.name)
                try:
                    fashion = Fashions.objects.get(cats_id=cats_item.fashions.id)
                except Fashions.DoesNotExist:
                    print('----- category error ----', cats_size.category.name)
                    continue
                item = Items()
                item.cats_id = cats_item.id
                item.fashions = fashion
                item.name = cats_item.name
                item.image = cats_item.image
                item.count_of_pieces = 0
                item.added = cats_item.added
                item.save()

                for balances in CatsBalance.objects.using('cats').filter(item=cats_item):
                    try:
                        size = Sizes.objects.get(cats_id=balances.size.id)
                    except Fashions.DoesNotExist:
                        print('----- balances error ----', cats_size.category.name)
                        continue
                    items_sizes = ItemsSizes()
                    items_sizes.items = item
                    items_sizes.sizes = size
                    items_sizes.save()
