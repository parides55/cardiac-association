# Generated by Django 5.1.1 on 2025-03-26 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0008_member_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='is_active',
            new_name='membership_status',
        ),
    ]
