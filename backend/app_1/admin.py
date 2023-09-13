from django.contrib import admin
from app_1.models import Nutrition, Product, ProductNutrition

admin.site.register(Nutrition)
admin.site.register(Product)
admin.site.register(ProductNutrition)