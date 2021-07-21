from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _

class Categories(models.Model):
    cats_id = models.PositiveIntegerField(_("cats_id"), default=None, blank=True)
    name = models.CharField(_("name"), max_length=70)
    image = ResizedImageField(size=[300, 150], upload_to="icons/", blank=True)
    image_hover = ResizedImageField(
        size=[300, 150], upload_to="icons/", blank=True
    )
    sequence = models.PositiveSmallIntegerField(_("sequence"), default=0)

    class Meta:
        ordering = ("sequence",)
        verbose_name = _("Categories of items")
        verbose_name_plural = _("Categories of items")

    def __str__(self):
        return u"%s" % self.name


class Fashions(models.Model):
    cats_id = models.PositiveIntegerField(_("cats_id"), default=None, blank=True)
    name = models.CharField(_("name"), max_length=70, default="No name")
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    image = ResizedImageField(size=[300, 150], upload_to="icons/", blank=True)
    image_hover = ResizedImageField(size=[300, 150], upload_to="icons/", blank=True)
    sequence = models.PositiveSmallIntegerField(_("sequence"), default=0)

    class Meta:
        ordering = ("sequence",)
        verbose_name = _("Fashions of items")
        verbose_name_plural = _("Fashions of items")

    def __str__(self):
        return u"%s" % self.name


class Sizes(models.Model):
    cats_id = models.PositiveIntegerField(_("cats_id"), default=None, blank=True)
    name = models.CharField(_("name"), max_length=20)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField(_("description"), blank=True, default="")
    sequence = models.PositiveSmallIntegerField(_("sequence"), default=0)

    class Meta:
        ordering = ("sequence",)
        verbose_name = _("Sizes of items")
        verbose_name_plural = _("Sizes of items")

    def __str__(self):
        return u"%s" % self.name


class Items(models.Model):
    cats_id = models.PositiveIntegerField(_("cats_id"), default=None, blank=True)
    name = models.CharField(_("name"), max_length=250)
    fashions = models.ForeignKey(Fashions, on_delete=models.CASCADE)
    image = ResizedImageField(size=[300, 300], upload_to="photos_items/",  blank=True)
    count_of_pieces = models.PositiveSmallIntegerField(_("count of pieces"), default=0)
    added = models.DateTimeField(_("added"))

    class Meta:
        ordering = ("name",)
        verbose_name = _("items")
        verbose_name_plural = _("items")

    def __str__(self):
        return u"%s (%s)" % (self.name, self.fashions.name)


class Pieces(models.Model):
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    sizes = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    detail = models.FileField(upload_to='all_details/')
    contour = models.FileField(upload_to='all_contours/')
    image = ResizedImageField(size=[100, 100], upload_to="photos_pieces/",  blank=True)

    class Meta:
        verbose_name = _("piece")
        verbose_name_plural = _("piece")

    def __str__(self):
        return u"%s piece (%s)" % (self.items.name, self.sizes.name)



class Produce_page(models.Model):
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    sizes = models.ForeignKey(Sizes, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("produce")
        verbose_name_plural = _("produce")

    def __str__(self):
        return u"%s item (%s)" % (self.items.name, self.sizes.name)