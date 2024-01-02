from django.contrib import admin
from app_1.models import *

admin.site.register(Nutrition)
admin.site.register(Product)
admin.site.register(ProductNutrition)
admin.site.register(Container)
admin.site.register(ContainerProduct)
admin.site.register(ContainerMass)