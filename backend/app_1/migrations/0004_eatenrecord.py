# Generated by Django 4.2 on 2023-09-27 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0003_alter_productnutrition_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='EatenRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_1.product')),
            ],
        ),
    ]