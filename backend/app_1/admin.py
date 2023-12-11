from django.contrib import admin
from app_1.models import Nutrition, Product, ProductNutrition, EatenRecord, Container, ContainerProduct, ContainerMass

admin.site.register(Nutrition)
admin.site.register(Product)
admin.site.register(ProductNutrition)
admin.site.register(EatenRecord)
admin.site.register(Container)
admin.site.register(ContainerProduct)
admin.site.register(ContainerMass)