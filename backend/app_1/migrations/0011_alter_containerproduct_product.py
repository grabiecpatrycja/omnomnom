# Generated by Django 4.2 on 2023-12-11 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0010_alter_containerproduct_container'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containerproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_containers', to='app_1.product'),
        ),
    ]