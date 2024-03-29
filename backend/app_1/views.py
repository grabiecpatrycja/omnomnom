from django.utils import timezone
from django.db import transaction
from django.db.models import Subquery, OuterRef, F, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app_1.models import *
from app_1.serializers import *


class NutritionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer

    def get_queryset(self):
        return Nutrition.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.prefetch_related("nutrition_entries__nutrition")
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["PUT"], serializer_class=ProductNutritionSerializer)
    @transaction.atomic
    def nutritions(self, request, pk=None):
        product = self.get_object()
        product_nutrition = ProductNutrition.objects.filter(product=product)
        product_nutrition.delete()

        for d in request.data:
            serializer = ProductNutritionSerializer(data=d, context={'request': request})

            serializer.is_valid(raise_exception=True)
            serializer.save(product=product)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], serializer_class=EatenRecordSerializer)
    def eat(self, request, pk=None):
        product = self.get_object()
        serializer = EatenRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mass = serializer.validated_data['mass']
        date = serializer.validated_data.get('date', timezone.now())

        second_later = date + timezone.timedelta(seconds=1)

        container = Container.objects.create(name=product, user=self.request.user)
        ContainerProduct.objects.create(container=container, product=product, mass=mass)
        ContainerMass.objects.create(container=container, mass=mass, date=date)
        ContainerMass.objects.create(container=container, mass=0, date=second_later)

        return Response(status=status.HTTP_201_CREATED)


class ContainerViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Container.objects.prefetch_related("product_entries__product")
    serializer_class = ContainerSerializer

    def get_queryset(self):
        return Container.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["PUT"], serializer_class=ContainerProductSerialzier)
    @transaction.atomic
    def products(self, request, pk=None):
        container = self.get_object()
        container_product = ContainerProduct.objects.filter(container=container)
        container_product.delete()

        for d in request.data:
            serializer = ContainerProductSerialzier(data=d, context={'request': request})

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

class log(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        containers_id = request.GET.getlist("containers")

        if Container.objects.filter(user=self.request.user, id__in=containers_id).count() != len(containers_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        date_1 = timezone.now().date()
        o_container = OuterRef("container")

        mass_1 = Subquery(
            ContainerMass.objects.filter(container=o_container, date__date=date_1)
            .order_by("-date")
            .values("mass")[:1]
        )
        mass_2 = Subquery(
            ContainerMass.objects.filter(container=o_container, date__date__lt=date_1)
            .order_by("-date")
            .values("mass")[:1]
        )
        product_initial_mass = Subquery(
            ContainerProduct.objects.filter(container=o_container)
            .values(
                "container",
            )
            .annotate(initial_mass=Sum("mass"))
            .values("initial_mass")[:1]
        )

        product_eaten = Subquery(
            ContainerProduct.objects.filter(
                container=o_container, product=OuterRef("product")
            )
            .annotate(eaten_mass=(mass_2 - mass_1) * F("mass") / product_initial_mass)
            .values("eaten_mass")[:1]
        )

        eaten_nutritions = (
            ProductNutrition.objects.values(
                "nutrition",
                "product",
                container=F("product__product_containers__container__id"),
            )
            .filter(container__in=containers_id)
            .annotate(eaten=product_eaten * F("value") / 100)
            .values(
                "nutrition",
            )
            .annotate(total_nutrition=Sum("eaten"))
        )

        return Response(eaten_nutritions)


