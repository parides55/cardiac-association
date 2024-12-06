# Generated by Django 5.1.1 on 2024-12-06 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingdetail',
            name='basket_items',
            field=models.ManyToManyField(related_name='shipping_items', to='shop.basket'),
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
