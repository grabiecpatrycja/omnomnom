# Generated by Django 4.2 on 2023-10-09 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0007_container_containerproduct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='containerproduct',
            old_name='value',
            new_name='mass',
        ),
    ]