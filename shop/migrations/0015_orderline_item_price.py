# Generated by Django 5.0 on 2024-01-30 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_remove_orderline_product_orderline_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='item_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
