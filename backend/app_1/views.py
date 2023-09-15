from rest_framework import viewsets
from app_1.models import Nutrition, Product
from app_1.serializers import NutritionSerializer, ProductSerializer

class NutritionViewSet(viewsets.ModelViewSet):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
