# Generated by Django 4.2.1 on 2023-06-01 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_brand_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='packing_cost',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.IntegerField(null=True),
        ),
    ]
