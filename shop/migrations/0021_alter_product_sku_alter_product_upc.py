# Generated by Django 5.0 on 2024-02-03 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_migrate_upc_and_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='upc',
            field=models.CharField(max_length=50),
        ),
    ]
