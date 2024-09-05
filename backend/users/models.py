from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    genders = [
        ('F', 'female'),
        ('M', 'male')
    ]

    PAL =[
        (1.4, 'very light'),
        (1.5, 'light'),
        (1.6, 'moderate'),
        (1.7, 'active'),
        (1.9, 'very active')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=genders, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    activity = models.CharField(max_length=10, choices=PAL, null=True, blank=True)
