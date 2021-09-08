from django.contrib import admin
from apps.orders.models import MaterialTypes, Rolls, Orders


class MaterialTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RollsAdmin(admin.ModelAdmin):
    list_display = ('material_type', 'initially_meters', 'actual_meters', 'date_of_purchase', 'index',)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('added', 'roll', 'amount_of_units', 'amount_of_material', 'expected_cost', 'actual_cost', 'date_of_manufacture', 'cost_rates',)

admin.site.register(MaterialTypes, MaterialTypesAdmin)
admin.site.register(Rolls, RollsAdmin)
admin.site.register(Orders, OrdersAdmin)
