# Generated by Django 5.1.1 on 2025-03-26 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0007_member_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_active',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('expired', 'Expired')], default='pending', max_length=20),
        ),
    ]
