# Generated by Django 5.1.1 on 2024-11-17 12:27

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('POSITIONS', models.IntegerField(choices=[(0, 'Chairman'), (1, 'Vice Chairman'), (2, 'Secretary'), (3, 'Assistant Secretary'), (4, 'Treasurer'), (5, 'Assistant Treasurer'), (6, 'Member'), (7, 'Staff')], default=0)),
            ],
        ),
    ]