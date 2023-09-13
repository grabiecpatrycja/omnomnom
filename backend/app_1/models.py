from django.db import models

class Nutrition(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class ProductNutrition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.nutrition}"