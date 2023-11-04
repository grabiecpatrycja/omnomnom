from django.db import transaction
from django.db.models import Subquery, OuterRef, F
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
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
        serializer.save(product=product)
        return Response(status=status.HTTP_201_CREATED)
    
class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.prefetch_related('product_entries__product')
    serializer_class = ContainerSerializer

    @action(detail=True, methods=['PUT'], serializer_class=ContainerProductSerialzier)
    @transaction.atomic
    def products(self, request, pk=None):
        container = self.get_object()
        for d in request.data:
            product = d.get('product')
            try:
                container_product = ContainerProduct.objects.get(container=container, product=product)
                serializer = ContainerProductSerialzier(container_product, data=d)
            except ContainerProduct.DoesNotExist:
                serializer = ContainerProductSerialzier(data=d)

            serializer.is_valid(raise_exception=True)
            serializer.save(container=container)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'], serializer_class=ContainerMassSerializer)
    def mass(self, request, pk=None):
        container = self.get_object()
        serializer = ContainerMassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(container=container)
        return Response(status=status.HTTP_201_CREATED)


#Próbuję robić rzeczy

# def mass_left(container):
#     first_mass = Subquery(ContainerMass.objects.filter(container=OuterRef('container')).order_by('date').values('mass')[:1])
#     mass_left = ContainerMass.objects.filter(container=container).order_by('-date').annotate(mass_left=first_mass-F('mass'))[:1]
#     return mass_left

# def eaten_today(container):
#     previous_mass = Subquery(ContainerMass.objects.filter(container=OuterRef('container'), date__lt=OuterRef('date')).order_by('-date').values('mass')[:1])
#     eaten_mass = ContainerMass.objects.filter(container=container).order_by('-date').annotate(eaten_today=previous_mass-F('mass'))
#     return eaten_mass 

# class log(APIView):

#     def get(self, request):
#         masses = eaten_today(2)
#         mass = [mass.eaten_today for mass in masses]
#         return Response(mass)




class log(APIView):

    def get(self, request):
        # robię to dla każdnego pojemnika w pętli?
        container = Container.objects.get(id=2)
        # obliczanie ilości zjedzonej danego dnia
        previous_mass = Subquery(ContainerMass.objects.filter(container=OuterRef('container'), date__lt=OuterRef('date')).order_by('-date').values('mass')[:1])
        eaten_mass = ContainerMass.objects.filter(container=container).order_by('-date').annotate(eaten_today=previous_mass-F('mass'))
        # znajdowanie z jakich produktów składa się container
        products = ContainerProduct.objects.filter(container=container)
        product_values = [product.value for product in products] # może by tu zrobić słownik


        product_list = [product.product.id for product in products]    
        masses = [mass.eaten_today for mass in eaten_mass]
        return Response(product_list)
