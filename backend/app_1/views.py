from rest_framework import viewsets
from app_1.models import Nutrition
from app_1.serializers import NutritionSerializer

class NutritionViewSet(viewsets.ModelViewSet):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer
