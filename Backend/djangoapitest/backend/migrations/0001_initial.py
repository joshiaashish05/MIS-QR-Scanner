# Generated by Django 4.2.2 on 2023-07-14 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "material_number",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("material_description", models.CharField(max_length=100)),
                ("material_group_number", models.IntegerField()),
                ("unit_of_measure", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Plant",
            fields=[
                (
                    "plantid",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("plantname", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("storedlocationtid", models.CharField(max_length=10)),
                ("storedlocationname", models.CharField(max_length=100)),
                (
                    "plant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="backend.plant"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CheckMaterial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("qty_material", models.DecimalField(decimal_places=2, max_digits=2)),
                ("unit_of_measure", models.CharField(max_length=10)),
                (
                    "stock_qty_material",
                    models.DecimalField(decimal_places=2, max_digits=2),
                ),
                ("last_update_stock_qty", models.DateTimeField()),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.material",
                    ),
                ),
                (
                    "plant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="backend.plant"
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="backend.store"
                    ),
                ),
            ],
        ),
    ]
