from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Nutrition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class ProductNutrition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="nutrition_entries")
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        unique_together = ["product", "nutrition"]

    def __str__(self):
        return f"{self.product} - {self.nutrition}"
   
class Container(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class ContainerProduct(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='product_entries')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_containers')
    mass = models.FloatField()

    class Meta:
        unique_together = ["container", "product"]

    def __str__(self):
        return f"{self.container} - {self.product}"
    
class ContainerMass(models.Model):
    container = models.ForeignKey(Container, on_delete=models.PROTECT)
    mass = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.container} - {self.mass}"