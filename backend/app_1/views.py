from rest_framework import viewsets
from .models import Nutrition
from .serializers import NutritionSerializer

class NutritionViewSet(viewsets.ModelViewSet):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer
