from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.nest.models import ItemsSizes


class MaterialTypes(models.Model):
    name = models.CharField(_("material type"), max_length=250)

    class Meta:
        verbose_name = _("material type")
        verbose_name_plural = _("material type")

    def __str__(self):
        return self.name


class Rolls(models.Model):
    index = models.CharField(_("index"), max_length=5)
    material_type = models.ForeignKey(MaterialTypes, on_delete=models.CASCADE)
    initially_meters = models.DecimalField(_("initially meters"), max_digits=5, decimal_places=2)
    actual_meters = models.DecimalField(_("actual meters"), max_digits=5, decimal_places=2)
    date_of_purchase = models.DateTimeField(_("date of manufacture"))

    class Meta:
        verbose_name = _("rolls")
        verbose_name_plural = _("rolls")

    def __str__(self):
        return self.material_type.name + " " + str(self.actual_meters)


class Orders(models.Model):
    cost_rates = models.DecimalField(_("coast rate"), max_digits=5, decimal_places=2)
    added = models.DateTimeField(_("added"), auto_now_add=True)
    roll = models.ForeignKey(Rolls, on_delete=models.CASCADE)
    amount_of_units = models.PositiveSmallIntegerField(_("amount of units"), default=0)
    amount_of_material = models.DecimalField(_("amount of material"), max_digits=5, decimal_places=2)
    expected_cost = models.DecimalField(_("expected cost"), max_digits=5, decimal_places=2)
    actual_cost = models.DecimalField(_("actual cost"), max_digits=5, decimal_places=2)
    date_of_manufacture = models.DateTimeField(_("date of manufacture"))
    paid = models.BooleanField(_("Paid or not"), default=False)
    image_preview = models.FileField(upload_to="photos_orders/", blank=True)

    class Meta:
        ordering = ("added",)
        verbose_name = _("orders")
        verbose_name_plural = _("orders")

    def __str__(self):
        return str(self.added)


class ClothesInOrders(models.Model):
    items_sizes = models.ForeignKey(ItemsSizes, on_delete=models.CASCADE, default=None, blank=True)
    amount = models.PositiveSmallIntegerField(_("amount"), default=0)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None, blank=True)

    class Meta:
        verbose_name = _("produce")
        verbose_name_plural = _("produce")

    def __str__(self):
        return str(self.order_id)


class GlobalSettings(models.Model):
    result_tif_path = models.CharField(_("tif_path"), max_length=256)
    jpeg_path = models.CharField(_("tif_path"), max_length=256)