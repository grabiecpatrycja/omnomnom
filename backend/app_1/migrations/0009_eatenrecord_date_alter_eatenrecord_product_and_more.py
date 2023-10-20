# Generated by Django 4.2 on 2023-10-20 12:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0008_rename_value_containerproduct_mass'),
    ]

    operations = [
        migrations.AddField(
            model_name='eatenrecord',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='eatenrecord',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_1.product'),
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
    ]