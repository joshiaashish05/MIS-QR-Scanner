from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# models.py
class Plant(models.Model):
    plantid = models.CharField(max_length=10, primary_key=True)
    plantname = models.CharField(max_length=100)

    def __str__(self):
        return self.plantname

class Store(models.Model):
    storedlocationtid = models.CharField(max_length=10)
    storedlocationname = models.CharField(max_length=100)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return self.storedlocationname

class Material(models.Model):
    material_number = models.CharField(max_length=20, primary_key=True)
    material_description = models.CharField(max_length=100)
    material_group_number = models.IntegerField()
    unit_of_measure = models.CharField(max_length=10)

    def __str__(self):
        return self.material_number

class CheckMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    qty_material = models.DecimalField(max_digits=100, decimal_places=2)
    unit_of_measure = models.CharField(max_length=10)
    stock_qty_material = models.DecimalField(max_digits=100, decimal_places=2)
    last_update_stock_qty = models.DateTimeField()

    def __str__(self):
        return f"{self.material.material_number} - {self.material.material_description}"

    @classmethod
    def get_check_materials(cls):
        return cls.objects.select_related('material', 'plant', 'store').values(
            'plant__plantid',
            'plant__plantname',
            'store__storedlocationtid',
            'store__storedlocationname',
            'material__material_number',
            'material__material_description',
            'material__material_group_number',
            'qty_material',
            'unit_of_measure',
            'stock_qty_material',
            'last_update_stock_qty'
        )


class CheckMaterialHistory(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    qty_material = models.DecimalField(max_digits=100, decimal_places=2)
    unit_of_measure = models.CharField(max_length=10)
    stock_qty_material = models.DecimalField(max_digits=100, decimal_places=2)
    last_update_stock_qty = models.DateTimeField()


    def __str__(self):
        return f"{self.material.material_number} - {self.material.material_description}"
