# Generated by Django 5.0 on 2024-02-01 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='default_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
