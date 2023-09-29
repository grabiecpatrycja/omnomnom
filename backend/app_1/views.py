from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app_1.models import Nutrition, Product, ProductNutrition
from app_1.serializers import NutritionSerializer, ProductSerializer, ProductNutritionSerializer, EatenRecordSerializer

class NutritionViewSet(viewsets.ModelViewSet):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['PUT'], serializer_class=ProductNutritionSerializer)
    @transaction.atomic
    def nutritions(self, request, pk=None):
        product = self.get_object()
        data = request.data
        for d in data:
            nutrition = d.get('nutrition')
            try:
                product_nutrition = ProductNutrition.objects.get(product=product, nutrition=nutrition)
                serializer = ProductNutritionSerializer(product_nutrition, data=d)
            except ProductNutrition.DoesNotExist:
                serializer = ProductNutritionSerializer(data=d)

            serializer.is_valid(raise_exception=True)
            serializer.save(product=product)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'], serializer_class=EatenRecordSerializer)
    def eat(self, request, pk=None):
        product = self.get_object()
        serializer = EatenRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(status=status.HTTP_201_CREATED)