# Generated by Django 4.2 on 2023-11-04 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0009_eatenrecord_date_alter_eatenrecord_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containerproduct',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_entries', to='app_1.container'),
        ),
    ]
