# Generated by Django 5.0 on 2024-01-25 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_ordershippingaddress_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
