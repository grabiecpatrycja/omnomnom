# Generated by Django 4.2 on 2024-09-04 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activity',
            field=models.CharField(blank=True, choices=[(1.4, 'very light'), (1.5, 'light'), (1.6, 'moderate'), (1.7, 'active'), (1.9, 'very active')], max_length=10, null=True),
        ),
    ]
