# Generated by Django 4.2 on 2024-07-13 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='containermass',
            name='meal',
            field=models.CharField(choices=[('B', 'breakfast'), ('L', 'lunch'), ('D', 'dinner'), ('Sn', 'snack'), ('Su', 'supper')], default='B', max_length=10),
        ),
    ]
