# Generated by Django 5.1.1 on 2025-02-09 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_shippingdetail_is_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingdetail',
            old_name='address',
            new_name='address_for_delivery',
        ),
    ]
