from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Plant, Store, CheckMaterial, CheckMaterialHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('plantid', 'plantname')
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('storedlocationtid', 'storedlocationname')
class MaterialSerializer(serializers.ModelSerializer):
    material = serializers.SerializerMethodField()

    def get_material(self, obj):
        material_obj = obj.material
        return {
            'material_number': material_obj.material_number,
            'material_description': material_obj.material_description,
            'material_group_number': material_obj.material_group_number,
            'unit_of_measure': material_obj.unit_of_measure,
        }

    class Meta:
        model = CheckMaterial
        fields = ('material', 'qty_material', 'stock_qty_material', 'last_update_stock_qty')
class CheckMaterialHistorySerializer(serializers.ModelSerializer):
    material_number = serializers.CharField(source='material.material_number')
    material_description = serializers.CharField(source='material.material_description')
    material_group_number = serializers.IntegerField(source='material.material_group_number')
    unit_of_measure = serializers.CharField(source='material.unit_of_measure')
    user = UserSerializer()
    store = StoreSerializer()
    plant = PlantSerializer()

    class Meta:
        model = CheckMaterialHistory
        fields = [
            'id',
            'user',
            'store',
            'plant',
            'qty_material',
            'unit_of_measure',
            'stock_qty_material',
            'last_update_stock_qty',
            'material_number',
            'material_description',
            'material_group_number'
        ]