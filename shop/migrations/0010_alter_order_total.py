# Generated by Django 5.0 on 2024-01-26 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_orderline_line_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Order total'),
        ),
    ]
