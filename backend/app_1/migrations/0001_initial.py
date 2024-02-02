# Generated by Django 4.2 on 2024-02-02 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContainerMass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_1.container')),
            ],
        ),
        migrations.CreateModel(
            name='ProductNutrition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('nutrition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_1.nutrition')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutrition_entries', to='app_1.product')),
            ],
            options={
                'unique_together': {('product', 'nutrition')},
            },
        ),
        migrations.CreateModel(
            name='ContainerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass', models.FloatField()),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_entries', to='app_1.container')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_containers', to='app_1.product')),
            ],
            options={
                'unique_together': {('container', 'product')},
            },
        ),
    ]
