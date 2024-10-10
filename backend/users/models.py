from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    class GenderChoices(models.TextChoices):
        FEMALE = 'F', 'female'
        MALE = 'M', 'male'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    activity = models.FloatField(null=True, blank=True)
