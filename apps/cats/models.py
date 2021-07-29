from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _

class Categories(models.Model):
    name = models.CharField(_("name"), max_length=70)
    image = ResizedImageField(size=[300, 150], upload_to="icons/", blank=True)
    image_hover = ResizedImageField(
        size=[300, 150], upload_to="icons/", blank=True
    )
    sequence = models.PositiveSmallIntegerField(_("sequence"), default=0)

    class Meta:
        db_table = "elephants_categories"
        managed = False


class Fashions(models.Model):
    name = models.CharField(_("name"), max_length=70, default="No name")
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    image = ResizedImageField(size=[300, 150], upload_to="icons/", blank=True)
    image_hover = ResizedImageField(size=[300, 150], upload_to="icons/", blank=True)
    sequence = models.PositiveSmallIntegerField(_("sequence"), default=0)

    class Meta:
        db_table = "elephants_fashions"
        managed = False


class Sizes(models.Model):
    name = models.CharField(_("name"), max_length=20)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField(_("description"), blank=True, default="")
    sequence = models.PositiveSmallIntegerField(_("sequence"), default=0)

    class Meta:
        db_table = "elephants_sizes"
        managed = False


class Items(models.Model):
    name = models.CharField(_("name"), max_length=250)
    fashions = models.ForeignKey(Fashions, on_delete=models.CASCADE)
    image = ResizedImageField(size=[300, 300], upload_to="photos/",  blank=True)
    added = models.DateTimeField(_("added"))

    class Meta:
        db_table = "elephants_items"
        managed = False


class Balance(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)

    class Meta:
        db_table = "elephants_balance"
        managed = False