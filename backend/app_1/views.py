from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app_1.models import Nutrition, Product, ProductNutrition
from app_1.serializers import NutritionSerializer, ProductSerializer, ProductNutritionSerializer

class NutritionViewSet(viewsets.ModelViewSet):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['PUT'], serializer_class=ProductNutritionSerializer)
    
    def nutritions(self, request, pk=None, nutrition_pk=None):
        data = request.data
        nutrition = data.get('nutrition')
        product = Product.objects.get(pk=pk)

        try:
            product_nutrition = ProductNutrition.objects.get(product=product, nutrition=nutrition)
            serializer = ProductNutritionSerializer(product_nutrition, data=data)
        except ProductNutrition.DoesNotExist:
            serializer = ProductNutritionSerializer(data=data)

        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)