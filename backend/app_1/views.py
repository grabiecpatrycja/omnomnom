from django.utils import timezone
from django.db import transaction
from django.db.models import Subquery, OuterRef, F, Sum
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

class log(APIView):

    def get(self, request):
        date_1 = timezone.now().date()

        mass_1 = Subquery(ContainerMass.objects.filter(container__product_entries__container=OuterRef('product'), date__date=date_1).order_by('-date').values('mass')[:1])
        mass_2 = Subquery(ContainerMass.objects.filter(container__product_entries__product=OuterRef('product'), date__date__lt=date_1).order_by('-date').values('mass')[:1])
        sum_container = ContainerProduct.objects.values('container').annotate(sum=Sum('mass'))
        masses = ContainerProduct.objects.annotate(eaten_mass=(mass_2-mass_1)*F('mass')/Subquery(sum_container.filter(container=F('container')).values('sum')[:1]))
        eaten_nutritions = ProductNutrition.objects.annotate(eaten=Subquery(masses.filter(product=F('product')).values('eaten_mass')[:1])*F('value')/100)
        sums = eaten_nutritions.values('nutrition').annotate(sum=Sum('eaten')).order_by()

        return Response(sums)
        
