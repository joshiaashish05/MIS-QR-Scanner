from django.contrib import admin


from django.contrib import admin
from .models import Plant, Store, Material, CheckMaterial, CheckMaterialHistory

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('plantid', 'plantname')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('storedlocationtid', 'storedlocationname', 'plant')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material_number', 'material_description', 'material_group_number','unit_of_measure')

@admin.register(CheckMaterial)
class CheckMaterialAdmin(admin.ModelAdmin):
    list_display = ('material', 'plant', 'store', 'qty_material', 'stock_qty_material', 'last_update_stock_qty')

class CheckMaterialHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'material',
        'plant',
        'store',
        'qty_material',
        'unit_of_measure',
        'stock_qty_material',
        'last_update_stock_qty',
        'user'
    )
    list_filter = ('plant', 'store', 'user')
    search_fields = (
        'material__material_number',
        'material__material_description',
        'user__username'
    )

admin.site.register(CheckMaterialHistory, CheckMaterialHistoryAdmin)
