# Generated by Django 5.0 on 2024-01-31 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_orderline_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
