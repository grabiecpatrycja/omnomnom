# Generated by Django 4.2.3 on 2023-12-19 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0011_alter_containerproduct_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containerproduct',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='containers_entries', to='app_1.container'),
        ),
    ]