from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    class GenderChoices(models.TextChoices):
        FEMALE = 'F', 'female'
        MALE = 'M', 'male'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    weight = models.FloatField(blank=True)
    height = models.FloatField(blank=True)
    birthdate = models.DateField(blank=True)
    activity = models.FloatField(blank=True)
