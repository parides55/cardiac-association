# Generated by Django 5.1.1 on 2024-11-27 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='excerpt',
            new_name='location',
        ),
    ]
