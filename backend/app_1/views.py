from datetime import datetime, timedelta
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app_1.models import *
from app_1.serializers import *

class NutritionViewSet(viewsets.ModelViewSet):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('nutrition_entries__nutrition')
    serializer_class = ProductSerializer

    @action(detail=True, methods=['PUT'], serializer_class=ProductNutritionSerializer)
    @transaction.atomic
    def nutritions(self, request, pk=None):
        product = self.get_object()
        for d in request.data:
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

        mass = serializer.validated_data['mass']
        date = serializer.validated_data.get('date', timezone.now())

        second_later = date + timezone.timedelta(seconds=1)

        container = Container.objects.create(name=product)
        ContainerProduct.objects.create(container=container, product=product, mass=mass)
        ContainerMass.objects.create(container=container, mass=mass, date=date)
        ContainerMass.objects.create(container=container, mass=0, date=second_later)

        return Response(status=status.HTTP_201_CREATED)
    
class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.prefetch_related('product_entries__product')
    serializer_class = ContainerSerializer

    @action(detail=True, methods=['PUT'], serializer_class=ContainerProductSerialzier)
    @transaction.atomic
    def products(self, request, pk=None):
        container = self.get_object()
        container_product = ContainerProduct.objects.filter(container=container)
        container_product.delete()

        for d in request.data:
            serializer = ContainerProductSerialzier(data=d)

            serializer.is_valid(raise_exception=True)
            serializer.save(container=container)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['GET','POST'], serializer_class=ContainerMassSerializer)
    def mass(self, request, pk=None):
        container = self.get_object()
        if request.method == 'GET':
            container_mass = ContainerMass.objects.filter(container=container)
            serializer = ContainerMassSerializer(container_mass, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if request.method == 'POST':
            serializer = ContainerMassSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(container=container)
            return Response(status=status.HTTP_201_CREATED)